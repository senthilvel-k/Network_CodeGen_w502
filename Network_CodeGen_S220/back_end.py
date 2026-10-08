                   
from cogent_gui import webgui as htmlPy
import json
import os
from PySide6 import QtGui, QtWidgets

''' This the Backend HTML application controlling the GUI portion '''

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
    
    @htmlPy.Slot()
    def save_cfg(self):
        file_path = os.path.realpath(__file__)
        import zipfile,glob,datetime,re
        
        time_now = str(datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S'))
        #time_str = re.sub('[:.]', '_', time_now)
        #app.evaluate_javascript("var cfg=prompt('Enter project configuration name');")
        app.evaluate_javascript("alert('Configuration saved successfully')")
        cfg_name=str(time_now)+'.cfg'#app.evaluate_javascript("cfg")+'.cfg'
        dir = './Config/'
        if not os.path.exists(dir):
          os.mkdir(dir)
        cfg_name=dir+cfg_name
        zip1=zipfile.ZipFile(cfg_name,'w',compression=zipfile.ZIP_DEFLATED)
        
        for files in glob.glob(r'.\html\*.html'):
            zip1.write(files)
        for files in glob.glob(r'.\data\*.data'):
            zip1.write(files)
        for files in glob.glob(r'.\js\*.js'):
            zip1.write(files)
        self.default_page()
        zip1.close()
       
        
    @htmlPy.Slot()
    def load_cfg(self):
        import zipfile
        window = QtWidgets.QMainWindow()
        file_val = QtWidgets.QFileDialog.getOpenFileName(window, "Select file", ".", "Config files (*.cfg);;All files (*.*)")[0]
        try:
            zip1 = zipfile.ZipFile(file_val)
            zip1.extractall()
            zip1.close()
            
            with open(self.__data_dir+"dbc_details.data",'r',encoding='utf-8') as data_file:
                dbc_details = json.loads(data_file.read())
            if dbc_details["ch0_file"] !='':
                self.__dbc=dbc_details["ch0_file"]
            if dbc_details["ch0_node_name"] !='':
                self.__node=dbc_details["ch0_node_name"]
             
            self.default_page()
            app.evaluate_javascript("alert('Configuration loaded successfully')")
        except:
            app.evaluate_javascript("alert('please choose proper config file')")
        

    
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
        
        temp_str = "var s=function(){document.getElementById('file_path').value='"+file_val+"';return false;};s();"
        app.evaluate_javascript(temp_str)     
    
    #for default display
    @htmlPy.Slot()
    def default_page(self):
        #print 'asdfa'
        app.template = ("Tool_Index_Page.html", {})
        #print self.__dbc ,self.__node,'-------------------------'
        
        if self.__dbc == None:
            self.__dbc = 'Select DBC'
        if self.__node == None:
            self.__dbc = 'None'
        temp_str = "var s=function(){document.getElementById('file_path').value='"+self.__dbc+"';document.getElementById('ch0_node_name').value='"+self.__node+"';return false;};s();"
        app.evaluate_javascript(temp_str) 
       
    #load dbc button configuration.
    @htmlPy.Slot(str, result=str)
    def upload_dbc(self,json_data):
        
        #print json
        data_file =open(self.__data_dir+'dbc_details.data','w',encoding='utf-8')
        data_file.write(json_data)
        data_file.close()
        data_file=open(self.__data_dir+"dbc_details.data",'r',encoding='utf-8')
        dbc_details = json.loads(data_file.read())
        #print dbc_details
        data_file.close()
        valid_check=0
        if dbc_details["ch0_file"] !='':
            self.__dbc=dbc_details["ch0_file"]
            valid_check=1
        else:
            valid_check=0
            app.evaluate_javascript("alert('Please enter valid dbc')")
            
        if dbc_details["ch0_node_name"] !='':
            self.__node=dbc_details["ch0_node_name"]
            self.__path=(self.__dbc)
            valid_check=1
        else:
            valid_check=0
            app.evaluate_javascript("alert('Please enter valid dbc')")
        
        if (self.__dbc!=None and self.__dbc!='' and self.__node!=None and self.__node != ''):
            try:
                from Dbc_Parser import dbc_parser
                x=dbc_parser(self.__dbc,self.__node)
                if x.check__node() == False:
                    valid_check=0
                    app.evaluate_javascript("alert('ERROR! Please Enter Proper node name')")
                if x.check_parsing() == False:
                    valid_check=0
                    app.evaluate_javascript("alert('ERROR! Please Enter Proper dbc')")
            except:
                valid_check=0
                app.evaluate_javascript("alert('ERROR! Please Enter Proper dbc/node name')")
        if valid_check == 1:
            self.__load=0
            app.evaluate_javascript("alert('Database loaded successfully')")
            
            
    #code generate button callback
    @htmlPy.Slot()
    def code_gen(self):
        if self.__load == 0:
            if (self.__msg_saved==0 and self.__sig_saved==0 ):
                #if (1):
                try:
                    import datetime
                    time_print = datetime.datetime.now()
                    
                    import can_rx_filt_gen as filter
                    filter.set_file_node_il(self.__dbc,self.__node)
                    filter.set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
                    filter.filter_gen()
                    
                    import msg as mes_struct
                    mes_struct.set_file_node_il(self.__dbc,self.__node)
                    mes_struct.set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
                    mes_struct.msg_struct_generation()
                    
                    import il_par_h_generation as il_h
                    il_h.set_file_node_il(self.__dbc,self.__node)
                    il_h.set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
                    il_h.il_par_h_gen_function()
                    
                    import il_par_c_generation as il_c
                    il_c.set_file_node_il(self.__dbc,self.__node)
                    il_c.set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
                    il_c.il_par_c_gen_function()
                    
                    
                    #Android Code Generation Part by Reegan(mreegan@visteon.com)
                    # import w601_parser_generation as w601_par
                    # w601_par.set_file_node_il(self.__path,self.__node)
                    # w601_par.set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
                    # w601_par.signal_get_Put(time_print.strftime("%Y-%m-%d %H:%M"))
                    # # w601_par.can_parser(time_print.strftime("%Y-%m-%d %H:%M"))
                    # w601_par.default_parser()
                    # w601_par.dbc_obj_update()
                    # w601_par.types_hal_parser()
                    '''import w601_parser_gen as w601_par
                    w601_par.set_file_node_il(self.__path,self.__node)
                    w601_par.set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
                    # w601_par.tx_buf_rx_buf_obj()
                    w601_par.can_parser()
                    w601_par.default_parser()
                    w601_par.types_hal_parser()
                    w601_par.releaseNotes()
                    '''

                    import vnim_app_signals_par as vnim_app
                    vnim_app.set_file_node_il(self.__dbc,self.__node)
                    vnim_app.set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
                    vnim_app.vnim_app_c_gen()
                    vnim_app.vnim_app_h_gen()
                    vnim_app.vnim_resource_gen()
                    vnim_app.nm_par_gen()
                    
                    app.evaluate_javascript("alert('Code Generated in CODE_GEN folder')")
                    
                except Exception as e:
                    import sys
                    sys.stdout = sys.__stdout__
                    if not os.path.exists('./CODE_GEN'):
                        os.mkdir('./CODE_GEN')
                    f = open('./CODE_GEN/errorlog.txt', 'w', encoding='utf-8')
                    f.write(str(e))
                    f.close()
                    app.evaluate_javascript("alert('ERROR! Please check the database file')")

                    app.evaluate_javascript("alert('ERROR! Please check the database file')")
            else:
                
                app.evaluate_javascript("alert('Please save Filter, message and signal configurations before generating the code')")

        else:
            app.evaluate_javascript("alert('Please Click load button to load dbc!!')")
            
        self.default_page()
                

    
    #message dbc configuration
    @htmlPy.Slot()
    def Can_dbc0_msg(self):
        if self.__path != '' and self.__path != None :
            try:
                import Can_dbc_gen as dbc_gen
                dbc_gen.html_mes(self.__dbc,self.__node)
                self.__msg_saved=1
                html_file=open(self.__html_dir+'CanDbcMsgConfiguration.html',encoding='latin-1')
                jscript_file=open(self.__java_dir+'CanDbcMsgConfiguration.js',encoding='latin-1')
                try: 
                    data_file =open(self.__data_dir+'CanDbcMsgConfiguration.data',encoding='latin-1')
                    #print "adfsfasfasfasdfasdfasdf"
                except:
                    data_file=None
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
            except:
                app.evaluate_javascript("alert('Load dbc file / enter proper node name @1')")
        else:
            app.evaluate_javascript("alert('Load dbc file / enter proper node name @2')")
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
        if self.__path != '' and self.__path != None:
          if (self.__msg_saved == 0):
            try:
                self.__sig_saved=1
                
                import Can_dbc_gen as dbc_gen
                dbc_gen.html_sig(self.__dbc,self.__node)
                html_file=open(self.__html_dir+'CanDbcSigConfiguration.html',encoding='latin-1')
                jscript_file=open(self.__java_dir+'CanDbcSigConfiguration.js',encoding='latin-1')
                try: 
                    data_file =open(self.__data_dir+'CanDbcSigConfiguration.data',encoding='latin-1')
                except:
                    data_file=' '
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
            except:
                app.evaluate_javascript("alert('Load dbc file / enter proper node name @3')")
          else:
            app.evaluate_javascript("alert('Please save message configuration and then select signal configuration')")
        else:
            app.evaluate_javascript("alert('Load dbc file / enter proper node name @4')")
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
        if self.__path != '' and self.__path != None:
            #try:
                self.__filter_saved=1
                import Can_filter_python_gen as filter
                #file1=open('FF_Door.dbc','DDP')

                filter.html(self.__dbc,self.__node)
                html_file=open(self.__html_dir+'CanFilterConfiguration.html',encoding='latin-1')
                jscript_file=open(self.__java_dir+'CanFilterConfiguration.js',encoding='latin-1')
                #data_file =open(self.__data_dir+'CanFilterConfiguration.data')
                
                try: 
                    data_file =open(self.__data_dir+'CanFilterConfiguration.data',encoding='latin-1')
                except:
                    data_file=' '
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
            #except:
                app.evaluate_javascript("alert('Load dbc file / enter proper node name @5')")
        else:
            app.evaluate_javascript("alert('Load dbc file / enter proper node name @6')")
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
        #print "asdfads"
        data_file=open("./data/dbc_details.data",'r',encoding='utf-8')
        dbc_details = json.loads(data_file.read())
        #print dbc_details
        data_file.close()

        if "ch0_file" in dbc_details:
            if dbc_details["ch0_file"] !='':
                dbc_name=dbc_details["ch0_file"]
                self.__path = dbc_details["ch0_file"]
                
            if dbc_details["ch0_node_name"] !='':
                node_name=dbc_details["ch0_node_name"]
                self.__node=dbc_details["ch0_node_name"]
            
        #print dbc_name,node_name
        temp_str = "var s=function(){document.getElementById('file_path').value='"+dbc_name+"';document.getElementById('ch0_node_name').value='"+node_name+"';return false;};s();"
        app.evaluate_javascript(temp_str)
        

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



