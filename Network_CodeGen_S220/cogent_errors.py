"""User-facing error messages and developer logging for CoGeNT.

Popups show what failed, why, which file/input caused it and what to do; they never show a
Python traceback. The traceback and context go to logs/cogent.log (and, for code generation,
to CODE_GEN/errorlog.txt)."""
import datetime
import os
import traceback

LOG_FILE = os.path.join('.', 'logs', 'cogent.log')

MSG_DATA_FILE = 'CanDbcMsgConfiguration.data'
SIG_DATA_FILE = 'CanDbcSigConfiguration.data'
MSG_PAGE = "+ TX/RX Message Configurations"
SIG_PAGE = "+ TX/Rx signal Configurations"

# Field suffixes of the keys in the saved .data files (see the generated configuration pages).
MESSAGE_FIELDS = ('msg_type_no_of_events', 'rx_key_msg', 'rx_ign_off', 'node_absent', 'msg_timeout',
                  'tx_enable', 'rx_enable', 'node_name', 'msg_dlc')
SIGNAL_FIELDS = ('os_notify_no_of_events', 'signal_fault_id', 'signal_content', 'rx_init_value',
                 'tx_init_value', 'green_drive', 'tx_debounce')


class CogentError(Exception):
    """An operation failed for a reason the user can act on (or an internal error, explained)."""

    def __init__(self, operation, reason, item=None, hint=None, log_path=None):
        super().__init__(reason)
        self.operation = operation
        self.reason = reason
        self.item = item
        self.hint = hint
        self.log_path = log_path

    def user_message(self):
        head = self.operation + " failed" + (" while " + self.item if self.item else "") + "."
        lines = [head, "Reason: " + self.reason.rstrip(".") + "."]
        if self.hint:
            lines.append(self.hint)
        if self.log_path:
            lines.append("Technical details: " + self.log_path)
        return "\n".join(lines)

    def __str__(self):
        return self.user_message()


def log_failure(operation, exc, context=None, extra_file=None):
    """Append the traceback and context to logs/cogent.log (and write extra_file if given).
    Returns the path the user should look at."""
    stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lines = ["=" * 78, "%s  %s failed" % (stamp, operation)]
    for key, value in (context or {}).items():
        lines.append("%s: %s" % (key, value))
    if isinstance(exc, CogentError):
        lines.append("Message shown to the user:")
        lines.append(exc.user_message())
        cause = exc.__cause__ or exc.__context__
        if cause is not None:
            lines.append("".join(traceback.format_exception(type(cause), cause, cause.__traceback__)))
    lines.append("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
    text = "\n".join(lines) + "\n"
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as fh:
            fh.write(text)
    except OSError:
        pass  # logging must never hide the original error
    if extra_file:
        try:
            os.makedirs(os.path.dirname(extra_file) or '.', exist_ok=True)
            with open(extra_file, 'w', encoding='utf-8') as fh:
                fh.write(text)
            return os.path.normpath(extra_file)
        except OSError:
            pass
    return os.path.normpath(LOG_FILE)


def split_config_key(key):
    """'VCU5_500_rx_enable' -> ('message', 'VCU5_500', 'rx_enable'); None if not a .data key."""
    for kind, fields in (('signal', SIGNAL_FIELDS), ('message', MESSAGE_FIELDS)):
        for field in fields:
            if key.endswith('_' + field) and len(key) > len(field) + 1:
                return kind, key[:-(len(field) + 1)], field
    return None


def missing_config_entry(key, output_file):
    """CogentError for a KeyError raised while a generator read the saved configuration."""
    parts = split_config_key(key)
    if parts is None:
        return None
    kind, name, field = parts
    data_file, page = (SIG_DATA_FILE, SIG_PAGE) if kind == 'signal' else (MSG_DATA_FILE, MSG_PAGE)
    return CogentError(
        "Code generation",
        "the saved %s configuration (data\\%s) has no '%s' setting for %s %s" % (kind, data_file, field, kind, name),
        item="generating " + output_file,
        hint="The configuration was probably saved for a different DBC, or the page was not saved after "
             "loading this DBC. Open '%s', check %s and press 'Save and Back', then run code gen again."
             % (page, name))
