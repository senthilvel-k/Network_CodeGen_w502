                   
from cogent_gui import webgui as htmlPy
import io
import json
import os
from PySide6 import QtGui, QtWidgets
import cogent_generate
from cogent_errors import CogentError, MSG_PAGE, SIG_PAGE, log_failure

''' This the Backend HTML application controlling the GUI portion '''


def _describe(exc):
    """Short, user-readable cause of an exception (no traceback)."""
    if isinstance(exc, FileNotFoundError):
        return "file not found: %s" % exc.filename
    if isinstance(exc, PermissionError):
        return "access denied to %s (is it open in another program or read-only?)" % exc.filename
    return "%s: %s" % (type(exc).__name__, exc)


def _open_data_or_empty(path):
    """Saved page settings, or an empty configuration when the page was never saved."""
    if not os.path.exists(path):
        return io.StringIO('{}')
    return open(path, encoding='latin-1')

class BackEnd(htmlPy.Object):
    
    __dbc=None
    __node=None
    __path=None
    __total_buf=32
    __basic_can_rx=4
    __basic_can_tx=4
    __remaining_buf=__total_buf-(__basic_can_tx+__basic_can_rx+4)
    __html_dir= './html/'
    __data_dir= './data/'
    __java_dir = './js/'
    
    #page save configuration 
    __drv_saved=0
    __disp_saved=0
    __il_saved=0
    __vnim_saved=0
    __msg_saved=1
    __sig_saved=1
    __filter_saved=1
    __load =1
    __unlock=0
    __password="pass"

    def _alert(self, text):
        app.evaluate_javascript("alert(%s)" % json.dumps(text))

    def _fail(self, operation, exc, reason=None, item=None, hint=None):
        """Log exc (with traceback) and show a popup without the traceback."""
        err = exc if isinstance(exc, CogentError) else CogentError(operation, reason or _describe(exc), item=item, hint=hint)
        if not err.log_path:
            err.log_path = log_failure(operation, exc, {"DBC file": self.__dbc, "Node": self.__node,
                                                        "Working folder": os.getcwd()})
        self._alert(err.user_message())

    def _not_loaded(self, operation):
        self._alert(CogentError(operation, "no DBC is loaded",
                                hint="Select the DBC file and the node name and press 'Load DBC' first.").user_message())

    def _set_fields(self, dbc, node):
        app.evaluate_javascript("document.getElementById('file_path').value=%s;document.getElementById('ch0_node_name').value=%s;"
                                % (json.dumps(dbc or ''), json.dumps(node or '')))
    
    @htmlPy.Slot()
    def save_cfg(self):
        file_path = os.path.realpath(__file__)
        import zipfile,glob,datetime,re
        
        time_now = str(datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S'))
        #time_str = re.sub('[:.]', '_', time_now)
        #app.evaluate_javascript("var cfg=prompt('Enter project configuration name');")
        cfg_name=str(time_now)+'.cfg'#app.evaluate_javascript("cfg")+'.cfg'
        dir = './Config/'
        cfg_name=dir+cfg_name
        try:
            if not os.path.exists(dir):
              os.mkdir(dir)
            with zipfile.ZipFile(cfg_name,'w',compression=zipfile.ZIP_DEFLATED) as zip1:
                for files in glob.glob(r'.\html\*.html'):
                    zip1.write(files)
                for files in glob.glob(r'.\data\*.data'):
                    zip1.write(files)
                for files in glob.glob(r'.\js\*.js'):
                    zip1.write(files)
        except OSError as exc:
            if os.path.isfile(cfg_name):
                os.remove(cfg_name)  # never leave a half-written archive
            self._fail("Saving the configuration", exc,
                       reason="%s could not be written (%s)" % (os.path.normpath(cfg_name), exc.strerror or exc),
                       item="writing the configuration archive",
                       hint="Check that 'Config' next to the tool is a writable folder (not a file and not read-only), then try again.")
            self.default_page()
            return
        self._alert("Configuration saved successfully\n" + os.path.abspath(cfg_name))
        self.default_page()


    @htmlPy.Slot()
    def load_cfg(self):
        import zipfile
        window = QtWidgets.QMainWindow()
        file_val = QtWidgets.QFileDialog.getOpenFileName(window, "Select file", ".", "Config files (*.cfg);;All files (*.*)")[0]
        if not file_val:
            return  # dialog cancelled
        op = "Loading the configuration"
        item = "reading " + os.path.basename(file_val)
        hint = "Choose a .cfg archive created with 'save_cofiguration' (they are kept in the Config folder)."
        try:
            # Check the archive before extracting, so a bad file cannot overwrite the current settings.
            with zipfile.ZipFile(file_val) as zip1:
                if 'data/dbc_details.data' not in zip1.namelist():
                    raise CogentError(op, "%s is a zip archive but not a CoGeNT configuration archive (data/dbc_details.data is missing)" % file_val,
                                      item=item, hint=hint)
                dbc_details = json.loads(zip1.read('data/dbc_details.data').decode('utf-8'))
                zip1.extractall()
        except CogentError as err:
            self._fail(op, err)
            return
        except zipfile.BadZipFile as exc:
            self._fail(op, exc, reason="%s is not a CoGeNT configuration archive (it is not a zip file)" % file_val, item=item, hint=hint)
            return
        except ValueError as exc:
            self._fail(op, exc, reason="data/dbc_details.data inside %s is damaged (%s)" % (file_val, exc), item=item, hint=hint)
            return
        except OSError as exc:
            self._fail(op, exc, reason=_describe(exc), item=item,
                       hint="Check that the archive can be read and that the html, data and js folders of the tool are writable.")
            return
        if dbc_details.get("ch0_file", '') !='':
            self.__dbc=dbc_details["ch0_file"]
        if dbc_details.get("ch0_node_name", '') !='':
            self.__node=dbc_details["ch0_node_name"]
        self.default_page()
        self._alert("Configuration loaded successfully\n%s\nPress 'Load DBC' before opening the configuration pages or running code gen." % file_val)



    @htmlPy.Slot()
    def unlock(self):
        if self.__unlock != 1:
            self.__password, _ok = QtWidgets.QInputDialog.getText(app.window, "Unlock", "Enter the password to unlock", QtWidgets.QLineEdit.EchoMode.Password)
            if self.__password == "canstack":
                self.__unlock = 1
                app.evaluate_javascript("alert('Generic configuration unlocked.')")
            else:
                self.__unlock = 0
                app.evaluate_javascript("alert('Invalid password.')")
        else:
            app.evaluate_javascript("alert('Already Configurations unlocked.')")
        
        
        
    @htmlPy.Slot()
    def file_browse(self):
        #print "button"
        window = QtWidgets.QMainWindow()
        file_val = QtWidgets.QFileDialog.getOpenFileName(window, "Select file", ".", "DBC files (*.dbc);;All files (*.*)")[0]
        #print file_val
        
        if not file_val:
            return  # dialog cancelled: keep the current path
        app.evaluate_javascript("document.getElementById('file_path').value=%s;" % json.dumps(file_val))
    
    #for default display
    @htmlPy.Slot()
    def default_page(self):
        #print 'asdfa'
        app.template = ("Tool_Index_Page.html", {})
        #print self.__dbc ,self.__node,'-------------------------'
        
        if self.__dbc or self.__node:
            self._set_fields(self.__dbc, self.__node)

    #load dbc button configuration.
    @htmlPy.Slot(str, result=str)
    def upload_dbc(self,json_data):
        op = "Loading the DBC"
        dbc_details = json.loads(json_data)
        try:
            with open(self.__data_dir+'dbc_details.data','w',encoding='utf-8') as data_file:
                data_file.write(json_data)
        except OSError as exc:
            log_failure(op + " (remembering the selection)", exc)  # not fatal for loading
        dbc = (dbc_details.get("ch0_file") or '').strip()
        node = (dbc_details.get("ch0_node_name") or '').strip()
        missing = [label for label, value in (("DBC File", dbc), ("Node Name", node)) if not value]
        if missing:
            self._alert(CogentError(op, "no %s was entered" % " and no ".join(missing),
                                    hint="Enter the DBC file (or use 'Browse ..') and the node name, then press 'Load DBC'.").user_message())
            return
        if not os.path.isfile(dbc):
            self._alert(CogentError(op, "DBC file not found: %s" % dbc,
                                    hint="Check the path or select the file with 'Browse ..', then press 'Load DBC' again.").user_message())
            return
        try:
            from Dbc_Parser import dbc_parser
            nodes = dbc_parser(dbc, node).get_nodes()
        except Exception as exc:
            self._fail(op, exc, reason="%s could not be read as a DBC file (%s)" % (dbc, _describe(exc)),
                       item="reading " + os.path.basename(dbc),
                       hint="Check that the file is a CAN database (.dbc) and is not damaged.")
            return
        if node not in nodes:
            known = ", ".join(nodes) if nodes else "none"
            self._alert(CogentError(op, "node '%s' is not defined in %s" % (node, os.path.basename(dbc)),
                                    hint="Nodes defined in this DBC (BU_ line): %s. Enter one of them as Node Name and press 'Load DBC' again." % known).user_message())
            return
        if (dbc, node) != (self.__dbc, self.__node):
            # Settings saved for another DBC/node do not match this one: the pages must be saved again.
            self.__msg_saved = 1
            self.__sig_saved = 1
        self.__dbc = dbc
        self.__node = node
        self.__path = dbc
        self.__load = 0
        self._alert("Database loaded successfully")


    #code generate button callback
    @htmlPy.Slot()
    def code_gen(self):
        op = "Code generation"
        if self.__load != 0:
            self._alert(CogentError(op, "no DBC is loaded",
                                    hint="Select the DBC file and the node name and press 'Load DBC', then open and save "
                                         "the configuration pages before running code gen.").user_message())
        elif self.__msg_saved != 0 or self.__sig_saved != 0:
            pages = [page for page, flag in ((MSG_PAGE, self.__msg_saved), (SIG_PAGE, self.__sig_saved)) if flag != 0]
            self._alert(CogentError(op, "the configuration of the loaded DBC has not been saved in this session: %s"
                                    % " and ".join("'%s'" % page for page in pages),
                                    hint="Open each page listed, check the settings and press 'Save and Back', then run code gen again.").user_message())
        else:
            import datetime
            time_print = datetime.datetime.now()
            try:
                files = cogent_generate.run_code_generation(self.__dbc, self.__node, time_print.strftime("%Y-%m-%d %H:%M"))
            except CogentError as err:
                self._alert(err.user_message())
            except Exception as exc:  # outside the generators (those are explained in cogent_generate)
                self._fail(op, exc, item="preparing the code generation",
                           hint="Please send logs\\cogent.log to the tool maintainer.")
            else:
                self._alert("Code Generated in CODE_GEN folder\n%d files written to %s"
                            % (len(files), os.path.abspath(cogent_generate.OUTPUT_DIR)))
        self.default_page()



    #message dbc configuration
    @htmlPy.Slot()
    def Can_dbc0_msg(self):
        if self.__load == 0 :
            try:
                import Can_dbc_gen as dbc_gen
                dbc_gen.html_mes(self.__dbc,self.__node)
                self.__msg_saved=1
                html_file=open(self.__html_dir+'CanDbcMsgConfiguration.html',encoding='latin-1')
                jscript_file=open(self.__java_dir+'CanDbcMsgConfiguration.js',encoding='latin-1')
                data_file =_open_data_or_empty(self.__data_dir+'CanDbcMsgConfiguration.data')
                #print  html_file.readlines() 
                final_data =(''.join( html_file.readlines() ))+"""<script>
        function load() {
        data=""" 
                
                if data_file !=None:
                    final_data=final_data+(''.join( data_file.readlines() ))+ """;"""+(''.join( jscript_file.readlines() ))+"""\nString.prototype.endsWith = function(suffix) {
            return this.indexOf(suffix, this.length - suffix.length) !== -1;
        };
        
        function enable_disable_key(elem){
        
        var sig = elem.split('_rx_key_msg')[0];
        if (document.getElementById(sig+'_msg_type_no_of_events'))
       {
          if (data[elem] == "on")
          {
            //document.getElementById(sig+'_msg_type_no_of_events').disabled = false;  
            document.getElementById(sig+'_node_absent').disabled = false;            
            document.getElementById(sig+'_node_absent').style.background = 'white';            
            document.getElementById(sig+'_msg_timeout').disabled = true;            
            document.getElementById(sig+'_msg_timeout').style.background = 'grey';       
          }
          else{   
            //document.getElementById(sig+'_msg_type_no_of_events').disabled = true;     
              document.getElementById(sig+'_node_absent').disabled = true;            
            document.getElementById(sig+'_node_absent').style.background = 'grey';            
            document.getElementById(sig+'_msg_timeout').disabled = false;             
            document.getElementById(sig+'_msg_timeout').style.background = 'white';
          }
      }
        
    };
    
    function tx_enable(elem){
    
    var sig = elem.id;
    sig=sig.split('_tx_enable')[0];
    
    if (elem.checked)
    {
         document.getElementById(sig+'_msg_type_no_of_events').style.background = 'white';            
         document.getElementById(sig+'_msg_type_no_of_events').disabled = false; 
    }
    else
    {
       document.getElementById(sig+'_msg_type_no_of_events').style.background = 'grey';            
       document.getElementById(sig+'_msg_type_no_of_events').disabled = true; 
    }
    
     
    };
    
         function rx_enable(elem){
        var child_text,idx,temp_str;
        var sig = elem.id;
        sig=sig.split('_rx_enable')[0];
        child_text=['_node_name','_rx_key_msg','_rx_ign_off','_msg_type_no_of_events','_msg_dlc','_msg_timeout','_node_absent'];
 
        if (elem.checked)
        {
          if (document.getElementById(sig+'_msg_type_no_of_events').value == "Appl")
          {
            for(idx=0;idx<child_text.length;idx++)
            { 
                  if((child_text[idx]!="_rx_key_msg") &&  (child_text[idx]!="_msg_timeout") && (child_text[idx]!="_node_absent"))
                  {
                    document.getElementById(sig+child_text[idx]).style.background = 'white';            
                    document.getElementById(sig+child_text[idx]).disabled = false; 
                  }
                  
                  if(child_text[idx]!="_rx_key_msg")
                  {
                    document.getElementById(sig+'_rx_key_msg').style.background = 'white';            
                    document.getElementById(sig+'_rx_key_msg').disabled = false; 
                
                    if (document.getElementById(sig+'_rx_key_msg').checked)
                    {
                      document.getElementById(sig+'_node_absent').disabled = false;            
                      document.getElementById(sig+'_node_absent').style.background = 'white';            
                      document.getElementById(sig+'_msg_timeout').disabled = true;            
                      document.getElementById(sig+'_msg_timeout').style.background = 'grey';    
                    }
                    else
                    {
                      document.getElementById(sig+'_node_absent').disabled = true;            
                      document.getElementById(sig+'_node_absent').style.background = 'grey';            
                      document.getElementById(sig+'_msg_timeout').disabled = false;             
                      document.getElementById(sig+'_msg_timeout').style.background = 'white';     
                    }
                  }
               }
           }
           else
           {
                  document.getElementById(sig+'_msg_type_no_of_events').disabled = false;            
                  document.getElementById(sig+'_msg_type_no_of_events').style.background = 'white';  
                  for(idx=0;idx<child_text.length;idx++)
                  {
                    if (child_text[idx] != '_msg_type_no_of_events')
                    {
                      temp_str=sig+child_text[idx];
                      document.getElementById(temp_str).disabled = true;            
                      document.getElementById(temp_str).style.background = 'grey';            
                    }
                  }
           }
        }
        else
        {   
            for(idx=0;idx<child_text.length;idx++)
            {
              temp_str=sig+child_text[idx];
              document.getElementById(temp_str).disabled = true;            
              document.getElementById(temp_str).style.background = 'grey';            
            } 
        }
    };
        function getClosest(el, tag) {
            // this is necessary since nodeName is always in upper case
            tag = tag.toUpperCase();
            do {
              if (el.nodeName === tag) {
                // tag name is found! let's return it. :)
                return el;
              }
            } while (el = el.parentNode);

            // not found :(
            return null;
          };
          
        var key,i,elem,elem2;
        key = Object.keys(data);
        //
        for ( i = 0, len = key.length; i < len; i++)
        {
             elem = document.getElementById(key[i]);
             if(document.getElementById(key[i]))
             {
                elem2=getClosest(elem,"tr");
                elem2.style.backgroundColor="#616161";
                if (document.getElementById(key[i]).type == "text")
                {
                  
                    elem.style.width=((parseInt(elem.value.length)+2)*9)+'px';
                }
             
            /*if ((key[i].endsWith("_rx_key_msg") != false)){
               //alert(key[i]);
               enable_disable_key(key[i]);
              }*/
              
              if((key[i].endsWith("_rx_enable") != false)){
              rx_enable(document.getElementById(key[i]));
              }
              
              if((key[i].endsWith("_tx_enable") != false)){
              tx_enable(document.getElementById(key[i]));
              }
              
              }
         }
         
         var tx_row,rx_row,elem_obj;
         tx_row =document.getElementById('tx_table').getElementsByTagName('tr');
         rx_row =document.getElementById('rx_table').getElementsByTagName('tr');
         //alert('Your table has ' + row_elem.length + ' rows.');
         for ( i = 2, len = (tx_row.length); i < len; i++)
         {
            //alert(key[0]);
            //alert("IS1_100_tx_enable" in data); 
            if(!(tx_row[i].id+"_tx_enable" in data))
            {
                elem_obj=getClosest((document.getElementById(tx_row[i].id+"_tx_enable")),"tr");
                elem_obj.style.backgroundColor="#3bb87e";
            }
         }
         for ( i = 2, len = (rx_row.length); i < len; i++)
         {
            if(!(rx_row[i].id+"_rx_enable" in data))
            {
                elem_obj=getClosest((document.getElementById(rx_row[i].id+"_rx_enable")),"tr");
                elem_obj.style.backgroundColor="#3bb87e";
            }
         }
         
};</script>"""
                new_file= open(self.__html_dir+'CAN_DBC_msg.html','w',encoding='latin-1')
                new_file.write(final_data)
                new_file.close()
                html_file.close()
                jscript_file.close()
                if data_file !=' ':
                    data_file.close()
                
                app.template = ("CAN_DBC_msg.html", {})
            except Exception as exc:
                self._fail("Opening '%s'" % MSG_PAGE, exc, item="building the page from " + os.path.basename(str(self.__dbc)),
                           hint="Check that the DBC file is still available and that the html, js and data folders of the tool are complete, then try again.")
        else:
            self._not_loaded("Opening '%s'" % MSG_PAGE)
            #app.template = ("CAN_DBC_msg.html", {})
            self.default_page()
    
    #Message save button configuration
    @htmlPy.Slot(str, result=str)        
    def Can_dbc_msg_SaveButton(self,json_data):
        self.__msg_saved=0
        data_file =open(self.__data_dir+'CanDbcMsgConfiguration.data','w',encoding='utf-8')
        data_file.write(json_data)
        data_file.close()
        self.default_page()
        
    
    #signal load configuration
    @htmlPy.Slot()   
    def Can_dbc0_sig(self):
        if self.__load == 0:
          if (self.__msg_saved == 0):
            try:
                self.__sig_saved=1
                
                import Can_dbc_gen as dbc_gen
                dbc_gen.html_sig(self.__dbc,self.__node)
                html_file=open(self.__html_dir+'CanDbcSigConfiguration.html',encoding='latin-1')
                jscript_file=open(self.__java_dir+'CanDbcSigConfiguration.js',encoding='latin-1')
                data_file =_open_data_or_empty(self.__data_dir+'CanDbcSigConfiguration.data')
                #print  html_file.readlines() 
                final_data =(''.join( html_file.readlines() ))+\
                """<script>
        window.onload = function() {
        data=""" 
                #print final_data
                if data_file !=' ':
                    final_data=final_data+(''.join( data_file.readlines() ))+ """;"""+(''.join(jscript_file.readlines() ))
                    final_data = final_data+'''\n'''+'''\nString.prototype.endsWith = function(suffix) {
            return this.indexOf(suffix, this.length - suffix.length) !== -1;
        };
        
        function signal_content_enable(elem){
    
          var sig = elem.id;
          sig=sig.split('_signal_content')[0];
          
          if (elem.checked)
          {
               document.getElementById(sig+'_signal_fault_id').style.background = 'white';            
               document.getElementById(sig+'_signal_fault_id').disabled = false; 
          }
          else
          {
             document.getElementById(sig+'_signal_fault_id').style.background = 'grey';            
             document.getElementById(sig+'_signal_fault_id').disabled = true; 
          }

          };
        
        function getClosest(el, tag) {
            // this is necessary since nodeName is always in upper case
            tag = tag.toUpperCase();
            do {
              if (el.nodeName === tag) {
                // tag name is found! let's return it. :)
                return el;
              }
            } while (el = el.parentNode);

            // not found :(
            return null;
          };
          
        var key,i,elem;
        key = Object.keys(data);
        //
        for ( i = 0, len = key.length; i < len; i++)
        {
             elem = document.getElementById(key[i])
             if(document.getElementById(key[i]))
             {
                if (document.getElementById(key[i]).type == "text")
                {
                  
                    elem.style.width=((parseInt(elem.value.length)+2)*9)+'px';
                }
             
               
              if((key[i].endsWith("_signal_content") != false)){
              signal_content_enable(document.getElementById(key[i]));
              }
              
            }
            else
            {
              
            }
         }
         
         var tx_row,rx_row,elem_obj;
         tx_row =document.getElementById('tx_table').getElementsByTagName('tr');
         rx_row =document.getElementById('rx_table').getElementsByTagName('tr');
         //alert('Your table has ' + row_elem.length + ' rows.');
         for ( i = 2, len = (tx_row.length); i < len; i++)
         {
            //alert(key[0]);
            //alert("IS1_100_tx_enable" in data); 
            if(!(tx_row[i].id+"_tx_init_value" in data))
            {
                elem_obj=getClosest((document.getElementById(tx_row[i].id+"_tx_init_value")),"tr");
                elem_obj.style.backgroundColor="#3bb87e";
            }
         }
         for ( i = 2, len = (rx_row.length); i < len; i++)
         {
            if(!(rx_row[i].id+"_rx_init_value" in data))
            {
                elem_obj=getClosest((document.getElementById(rx_row[i].id+"_rx_init_value")),"tr");
                elem_obj.style.backgroundColor="#3bb87e";
            }
         }
         
        };'''

                else:
                    final_data=final_data+(''.join( data_file))+ """];"""

                final_data+='''\n</script>'''
                new_file= open(self.__html_dir+'CAN_DBC_sig.html','w',encoding='latin-1')
                new_file.write(final_data)
                new_file.close()
                html_file.close()
                jscript_file.close()
                if data_file !=' ':
                    data_file.close()
                
                app.template = ("CAN_DBC_sig.html", {})
            except Exception as exc:
                self._fail("Opening '%s'" % SIG_PAGE, exc, item="building the page from " + os.path.basename(str(self.__dbc)),
                           hint="Check that the DBC file is still available and that the html, js and data folders of the tool are complete, then try again.")
          else:
            self._alert(CogentError("Opening '%s'" % SIG_PAGE, "the message configuration has not been saved in this session",
                                    hint="Open '%s' and press 'Save and Back' first: the signal page lists the signals of the enabled messages." % MSG_PAGE).user_message())
        else:
            self._not_loaded("Opening '%s'" % SIG_PAGE)
            #app.template = ("CAN_DBC_msg.html", {})
            self.default_page()
    #signals  save button
    
    @htmlPy.Slot(str, result=str)
    def Can_dbc0_sig_SaveButton(self,json_data):
        #print json_data
        self.__sig_saved=0
        data_file =open(self.__data_dir+'CanDbcSigConfiguration.data','w',encoding='utf-8')
        data_file.write(json_data)
        data_file.close()
        self.default_page()
    
          
    #filter configuraion load button
    @htmlPy.Slot()
    def Can_Filter(self):
        #print self.__dbc
        if self.__load == 0:
            try:
                self.__filter_saved=1
                import Can_filter_python_gen as filter
                #file1=open('FF_Door.dbc','DDP')

                filter.html(self.__dbc,self.__node)
                html_file=open(self.__html_dir+'CanFilterConfiguration.html',encoding='latin-1')
                jscript_file=open(self.__java_dir+'CanFilterConfiguration.js',encoding='latin-1')
                #data_file =open(self.__data_dir+'CanFilterConfiguration.data')
                
                data_file =_open_data_or_empty(self.__data_dir+'CanFilterConfiguration.data')
                #print  html_file.readlines() 
                final_data =(''.join( html_file.readlines() ))+\
                """<script>
        window.onload = function() {
        data=""" 
                #print final_data
                if data_file !=' ':
                    final_data=final_data+(''.join( data_file.readlines() ))+ """;"""+(''.join(jscript_file.readlines() ))
                    final_data = final_data+'''\n'''+'''
        
        '''

                else:
                    final_data=final_data+(''.join( data_file))+ """];"""
                final_data+='''\nString.prototype.endsWith = function(suffix) {
            return this.indexOf(suffix, this.length - suffix.length) !== -1;
        };
        
        function enable_disable(elem){
        
        var sig = elem.split('_enable')[0];
        if (document.getElementById(sig+'_msg_type_no_of_events'))
       {
          if (data[elem] == "on")
          {
            document.getElementById(sig+'_msg_type_no_of_events').disabled = false;            
          }
          else{   
            document.getElementById(sig+'_msg_type_no_of_events').disabled = true;         
          }
      }
        
    };
        var key,i;
        key = Object.keys(data);
        //
        for ( i = 0, len = key.length; i < len; i++)
        {
             
            if ((key[i].endsWith("_enable") != false)){
               //alert(key[i]);
               enable_disable(key[i]);
            
                
              }
         }'''
                final_data+='''};\n</script>'''
                
                new_file= open(self.__html_dir+'Can_filter.html','w',encoding='latin-1')
                new_file.write(final_data)
                new_file.close()
                html_file.close()
                jscript_file.close()
                data_file.close()
                app.template = ("Can_filter.html", {})
            except Exception as exc:
                self._fail("Opening the filter configuration page", exc, item="building the page from " + os.path.basename(str(self.__dbc)),
                           hint="Check that the DBC file is still available and that the html, js and data folders of the tool are complete, then try again.")
        else:
            self._not_loaded("Opening the filter configuration page")
            #app.template = ("CAN_DBC_msg.html", {})
            self.default_page()
        
    #filter save button callback
    @htmlPy.Slot(str, result=str)        
    def Filter_SaveButton(self,json_data):
        self.__filter_saved=0
        data_file =open(self.__data_dir+'CanFilterConfiguration.data','w',encoding='utf-8')
        data_file.write(json_data)
        data_file.close()
        self.default_page()

    #back button
    @htmlPy.Slot(str, result=str)
    def BackButton(self,json_data):
        #print "BackButton callback"     
        app.template = ("Tool_Index_Page.html", {})

    @htmlPy.Slot()        
    def pythonfn(self):
        app.evaluate_javascript("alert('Hello from back-end')")
    
    @htmlPy.Slot()      
    def onpageload(self):
        try:
            with open("./data/dbc_details.data",'r',encoding='utf-8') as data_file:
                dbc_details = json.loads(data_file.read())
        except FileNotFoundError:
            return  # nothing selected yet: leave the fields empty
        except ValueError as exc:
            self._fail("Restoring the last DBC selection", exc, reason="data\\dbc_details.data is damaged (%s)" % exc,
                       hint="Select the DBC file and node name again and press 'Load DBC'.")
            return
        dbc_name = dbc_details.get("ch0_file", '')
        node_name = dbc_details.get("ch0_node_name", '')
        if dbc_name !='':
            self.__path = dbc_name
        if node_name !='':
            self.__node = node_name
        self._set_fields(dbc_name, node_name)


app = htmlPy.AppGUI(title="CoGeNT")
app.maximized = True

base_dir=os.path.abspath(os.path.dirname(__file__))

app.template_path = os.path.join(base_dir, "html/")
app.static_path = os.path.join(base_dir, "style/")
app.window.setWindowIcon(QtGui.QIcon(os.path.join(base_dir, "batman.ico")))
app.right_click_setting(htmlPy.settings.DISABLE)
app.bind(BackEnd())
app.allow_overwrite=True
app.template = ("Tool_Index_Page.html", {})



