def html_mes(file_name,node):
    import os
    js ='\n'
    
    il_parser = 'GenMsgILSupport'
    nm_parser = 'NmMessage'
    all_parser = 'ALL'
    html_dir= './html/'
    data_dir= './data/'
    java_dir = './js/'
    
    html_css_content="""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Filter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script type="text/javascript" src="data.json"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="{{'styl.css'|staticfile }}">

   <script>
    function MakeWidth_bit_pos(elem){
        //var len_per=(parseInt(elem.value.length)
        elem.style.width=((parseInt(elem.value.length)+2)*9)+'px';
        /*if (elem.value!="")<=56)
        {
            elem.style.background="white";
         }
         else
         {
                alert("Enter Proper bit Position");
                elem.style.background="red";
         }
        */
                
        }
    </script>
    
    <script>
    function msg_type_clicked(elem){
     var child_text,idx,temp_str;
        var sig = elem.id;
        sig=sig.split('_msg_type_no_of_events')[0];
        child_text=['_node_name','_rx_key_msg','_rx_ign_off','_msg_dlc','_msg_timeout','_node_absent'];
 
        if (elem.value == 'Appl')
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
            for(idx=0;idx<child_text.length;idx++)
            {
              temp_str=sig+child_text[idx];
              document.getElementById(temp_str).disabled = true;            
              document.getElementById(temp_str).style.background = 'grey';            
            } 
        }
    };
    </script>
    
    <script>
    function tx_enable_clicked(elem){
    
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
    </script>
    
    <script>
    function rx_enable_clicked(elem){
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
    
    </script>
    
    <script>
    function rx_key_msg_clicked(elem){
        var sig = elem.id;
        sig=sig.split('_rx_key_msg')[0];
        if (elem.checked)
        {
            document.getElementById(sig+'_node_absent').disabled = false;            
            document.getElementById(sig+'_node_absent').style.background = 'white';            
            document.getElementById(sig+'_msg_timeout').disabled = true;            
            document.getElementById(sig+'_msg_timeout').style.background = 'grey';            
        }
        else{   
            document.getElementById(sig+'_node_absent').disabled = true;            
            document.getElementById(sig+'_node_absent').style.background = 'grey';            
            document.getElementById(sig+'_msg_timeout').disabled = false;             
            document.getElementById(sig+'_msg_timeout').style.background = 'white';        
        }
    };
    
    </script>
    </head>
    <body onload="load()" class="w3-container w3-grey">"""

    file1=open(html_dir+'Tool_Index_Page.html','r',encoding='latin-1')
    start=0
    for line in file1.readlines():
        if '<!--copy_start-->' == line.rstrip('\n'):
            start=1
        elif '<!--copy_end-->' == line.rstrip('\n'):
            start=0
        if start == 1:
            html_css_content=html_css_content+line

    file1.close()

    html_css_content = html_css_content + '<form action="BackEnd.Can_dbc_msg_SaveButton" id="form" data-bind="true">\n<label class="w3-label w3-text-light-grey">\
    <h1>Tx Messages</h1></label>'
    html_css_content = html_css_content + '<input type="submit" value="Save and Back" id="form_submit">'
    html_css_content = html_css_content+'''<table  id="tx_table" class ="w3-table  w3-bordered  w3-border w3-hoverable w3-small w3-centered ">
    <thead>
    <tr>
    <th text-align="center" rowspan="2">Message Name</th>
    <th colspan="3" > Message Properties</th>
    <th colspan="2" > Configuration Parameters</th>
    </tr>
    <tr>
    <th>ID</th>
    <th>DLC</th>
    <th>Periodicity</th>
    <th>Enable/Disable Message</th>
    <th>Message Type</th>
    
    </tr>
    </thead>    
    '''
   

    def html_print(msg_list,type,tx,enum):
        
        temp_html_css_content=''
        temp_js=' '
        #print msg_list
        #if type == 'APPL':
        for index in msg_list:
            
            temp_html_css_content = temp_html_css_content+'''<tr id="'''+index['Msg_name']+'''"><div>
            <td><label class="w3-label w3-text-light-grey" >'''+index['Msg_name']+'''</label></td>
            <td><label class="w3-label w3-text-light-grey" >'''+hex(int(index['id']))+'''</label></td>
            <td><label class="w3-label w3-text-light-grey" >'''+index['DLC']+'''</label></td>
            <td><label class="w3-label w3-text-light-grey" >'''+index['GenMsgCycleTime']+'''</label></td>'''
            if(0):
              if (tx=='tx'):
                if index['GenMsgSendType'].isalpha():
                  temp_html_css_content = temp_html_css_content+'''<td><label class="w3-label w3-text-light-grey" >'''+index['GenMsgSendType']+'''</label></td>'''
                else:
                  temp_html_css_content = temp_html_css_content+'''<td><label class="w3-label w3-text-light-grey" >'''+enum['GenMsgSendType'][int(index['GenMsgSendType'])]+'''</label></td>'''
                
            temp_html_css_content = temp_html_css_content+'\n'
            
            if (tx=='tx'):
                
                temp_sig_list=[x for x in index['Sig_List']]
                #get signal name in a list 
                #print index['Sig_List']
                check_box=['_tx_enable','_tx_precopy','_tx_confirmation']
                drop_down=[('_msg_type',['Appl','NM','Diag'])]
                
                for i in check_box[:1]:
                    temp_js=temp_js+'document.getElementById("'+index['Msg_name'].upper()+i+'").checked = (data.'+index['Msg_name'].upper()+i+' == "on" ? true : false);\n'
                    temp_html_css_content = temp_html_css_content+'''<td><input class="'''+i.lstrip('_')+'''" id="'''+index['Msg_name'].upper()+i+'''"  onclick="'''+i.lstrip('_')+'''_clicked(this)"  name="'''+index['Msg_name'].upper()+i+'''" checked="false" type="checkbox"></td>'''+'\n'
                
                
                for i in drop_down:
                    temp_html_css_content = temp_html_css_content+'''<td><select id="'''+index['Msg_name'].upper()+i[0]+'''_no_of_events" style="width:100" class="'''+str(index['Msg_name'].upper())+i[0]+'''_no_of_events "  name="'''+str(index['Msg_name'].upper())+i[0]+'''_no_of_events"  onchange="holder_clicked(this)" style="width:100%">'''
                    temp_js +='document.getElementById("'+index['Msg_name']+i[0]+'''_no_of_events'''+'").value = data.'+index['Msg_name']+i[0]+'_no_of_events;\n'
                    for no_of_event in range(len(i[1])):
                        temp_html_css_content+='<option value="'+i[1][no_of_event]+'">'+i[1][no_of_event]+'</option>\n'
                
                
                #print index
                
                
                temp_html_css_content = temp_html_css_content+'''</tr>
                </div>'''
           
            else:
                temp_sig_list=[x for x in index['Sig_List']]
                #get signal name in a list 
                #print index['Sig_List']
                check_box=['_rx_enable','_rx_key_msg','_rx_ign_off']
                drop_down=[('_msg_type',['Appl','NM','Diag'])]
                
                for i in check_box[:1]:
                    temp_js=temp_js+'document.getElementById("'+index['Msg_name'].upper()+i+'").checked = (data.'+index['Msg_name'].upper()+i+' == "on" ? true : false);\n'
                    temp_html_css_content = temp_html_css_content+'''<td><input class="'''+i.lstrip('_')+'''" id="'''+index['Msg_name'].upper()+i+'''"   name="'''+index['Msg_name'].upper()+i+'''" checked="false" onclick="'''+i.lstrip('_')+'''_clicked(this)" type="checkbox"></td>'''+'\n'
               
                
                for i in drop_down:
                    temp_html_css_content = temp_html_css_content+'''<td><select id="'''+index['Msg_name'].upper()+i[0]+'''_no_of_events" style="width:100"  class="'''+str(index['Msg_name'].upper())+i[0]+'''_no_of_events "  name="'''+str(index['Msg_name'].upper())+i[0]+'''_no_of_events"  onchange="msg_type_clicked(this)" style="width:100%">'''
                    temp_js +='document.getElementById("'+index['Msg_name'].upper()+i[0]+'''_no_of_events'''+'").value = data.'+index['Msg_name'].upper()+i[0]+'_no_of_events;\n'
                    for no_of_event in range(len(i[1])):
                        temp_html_css_content+='<option value="'+i[1][no_of_event]+'">'+i[1][no_of_event]+'</option>\n'
                            
                            
                temp_html_css_content+='''<td><input class="w3-input" id = "'''+str(index['Msg_name'].upper())+'''_node_name" name = "'''+str(index['Msg_name'].upper())+'''_node_name"  onblur="MakeWidth_bit_pos(this)" ></td>\n'''
                temp_js +='\n if  ("'+index['Msg_name'].upper()+'_node_name"  in data)\n {\n  document.getElementById("'+index['Msg_name'].upper()+'''_node_name'''+'").value = data.'+index['Msg_name'].upper()+'_node_name;\n}\n'
                
                for i in check_box[1:2]:
                    temp_js=temp_js+'document.getElementById("'+index['Msg_name'].upper()+i+'").checked = (data.'+index['Msg_name'].upper()+i+' == "on" ? true : false);\n'
                    temp_html_css_content = temp_html_css_content+'''<td><input class="'''+i.lstrip('_')+'''" id="'''+index['Msg_name'].upper()+i+'''"   name="'''+index['Msg_name'].upper()+i+'''" checked="false" onclick="'''+i.lstrip('_')+'''_clicked(this)" type="checkbox"></td>'''+'\n'
                #print index
                #node absent dtc
                temp_html_css_content+='''<td><input class="w3-input" id = "'''+str(index['Msg_name'].upper())+'''_node_absent" name = "'''+str(index['Msg_name'].upper())+'''_node_absent"   onblur="MakeWidth_bit_pos(this)" ></td>\n'''
                temp_js +='\n if  ("'+index['Msg_name'].upper()+'_node_absent"  in data)\n {\n  document.getElementById("'+index['Msg_name'].upper()+'''_node_absent'''+'").value = data.'+index['Msg_name'].upper()+'_node_absent;\n}\n'
                #timeout DTC
                temp_html_css_content+='''<td><input class="w3-input" id = "'''+str(index['Msg_name'].upper())+'''_msg_timeout" name = "'''+str(index['Msg_name'].upper())+'''_msg_timeout"  onblur="MakeWidth_bit_pos(this)" ></td>\n'''
                temp_js +='\n if  ("'+index['Msg_name'].upper()+'_msg_timeout"  in data)\n {\n  document.getElementById("'+index['Msg_name'].upper()+'''_msg_timeout'''+'").value = data.'+index['Msg_name'].upper()+'_msg_timeout;\n}\n'
                
                #dlc DTC
                temp_html_css_content+='''<td><input class="w3-input" id = "'''+str(index['Msg_name'].upper())+'''_msg_dlc" name = "'''+str(index['Msg_name'].upper())+'''_msg_dlc"  onblur="MakeWidth_bit_pos(this)" ></td>\n'''
                temp_js +='\n if  ("'+index['Msg_name'].upper()+'_msg_dlc"  in data)\n {\n  document.getElementById("'+index['Msg_name'].upper()+'''_msg_dlc'''+'").value = data.'+index['Msg_name'].upper()+'_msg_dlc;\n}\n'
                
                
                for i in check_box[2:]:
                    temp_js=temp_js+'document.getElementById("'+index['Msg_name'].upper()+i+'").checked = (data.'+index['Msg_name'].upper()+i+' == "on" ? true : false);\n'
                    temp_html_css_content = temp_html_css_content+'''<td><input class="'''+i.lstrip('_')+'''" id="'''+index['Msg_name'].upper()+i+'''"   name="'''+index['Msg_name'].upper()+i+'''" checked="false" onclick="'''+i.lstrip('_')+'''_clicked(this)" type="checkbox"></td>'''+'\n'
                
                
                
                            
                temp_html_css_content = temp_html_css_content+'''</tr>
                </div>'''
       
        #else:
        #    pass
            
            #parse_type = (Configuration_dict_map_range[index]).split('..')
        
        return (temp_html_css_content,temp_js)

    from Dbc_Parser import dbc_parser

    dbc=dbc_parser(file_name,node)
    #print dbc.get_msg_type('GenMsgIlSupport','tx')[0]
    enum = dbc.get_enum_values()
    il_tx =dbc.get_msg_type(all_parser,'tx')
    il_sorted_mes = sorted(il_tx,key = lambda x: x['Msg_name'])
    il_tx_fin=html_print(il_sorted_mes,'APPL','tx',enum)
    html_css_content=html_css_content+il_tx_fin[0]
    js=js+il_tx_fin[1]
    

    html_css_content=html_css_content+'</table><br><label class="w3-label w3-text-light-grey">\
    <h1>Rx Messages</h1></label>'

    html_css_content = html_css_content+'''
    <table id="rx_table" style="width:100%" class ="w3-table  w3-bordered  w3-border w3-hoverable w3-small w3-centered ">
    <thead>
    <tr>
    <th text-align="center" rowspan="2">Message Name</th>
    <th colspan="3" > Message Properties</th>
    <th colspan="9" > Configuration Parameters</th>
    </tr>
    <tr>
    <th>ID</th>
    <th>DLC</th>
    <th>Periodicity</th>
    <th>Enable/Disable Message</th>
    <th>Message Type</th>
    <th>Node Name</th>
    <th>Key Message</th>
    <th>Node Absent ID</th>
    <th>Message Timout ID</th>
    <th>Message Content DLC ID</th>
    <th>Notification during IGN OFF</th>
    <!--
    <th>OS Message Notification</th> 
    -->
    </tr>
    </thead>
    
    '''
    il_rx = dbc.get_msg_type(all_parser,'rx')
    il_sorted_mes = sorted(il_rx,key = lambda x: x['Msg_name'])
    il=html_print(il_sorted_mes,'APPL','rx',enum)
    html_css_content=html_css_content+il[0]
    
    js=js+il[1]
    
    #tp message
    #html_css_content=html_css_content+html_print(dbc.get_msg_type('NmMessage','tx'),'NM')
    #tp=html_print(dbc.get_msg_type('TpMessage','rx'),'DIAG','rx')
    #html_css_content=html_css_content+tp[0]
    #js=js+tp[1]
    
     
    html_css_content = html_css_content +""" </table>
    <br>
    <br>
    
    </form>
    </div> 
    </div> 
    </body>
    </html>
    """

    #print html_css_content
    html= open(html_dir+'CanDbcMsgConfiguration.html', 'w',encoding='latin-1')
    html.write(html_css_content)
    html.close()
    #print js
    jscript = open(java_dir+'CanDbcMsgConfiguration.js', 'w',encoding='latin-1')
   
    jscript.write(js)
    
    
    jscript.close()
    
def html_sig(file_name,node):
    html_dir= './html/'
    data_dir= './data/'
    java_dir = './js/'
    
    il_parser = 'GenMsgILSupport'
    nm_parser = 'NmMessage'
    full_msg = 'ALL'
    import os,json
    js ='\n'
    html_css_content="""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Filter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script type="text/javascript" src="data.json"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="{{'styl.css'|staticfile }}">
    
    <script>
    function accordionfn(id) {
        var x = document.getElementById(id);
        if (x.className.indexOf("w3-show") == -1) {
            x.className += " w3-show";
        } else { 
            x.className = x.className.replace(" w3-show", "");
        }
    }</script>
    
    <script>
    function signal_content_clicked(elem){
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
    
    </script>
    <script>
    function MakeWidth(elem)
    {
        elem.style.width=((parseInt(elem.value.length)+2)*9)+'px';  
    }
    </script>
    
    </head>
    <body onload="load()" class="w3-container w3-grey">"""

    file1=open(html_dir+'Tool_Index_Page.html','r',encoding='latin-1')
    start=0
    for line in file1.readlines():
        if '<!--copy_start-->' == line.rstrip('\n'):
            start=1
        elif '<!--copy_end-->' == line.rstrip('\n'):
            start=0
        if start == 1:
            html_css_content=html_css_content+line

    file1.close()

    html_css_content = html_css_content + '<form action="BackEnd.Can_dbc0_sig_SaveButton" id="form" data-bind="true">\n<label class="w3-label w3-text-light-grey">\
    <h1>Tx Signals</h1></label>'
    html_css_content = html_css_content + '<input type="submit" value="Save and Back" id="form_submit">'
    html_css_content = html_css_content+'''<table id="tx_table" class ="w3-table  w3-bordered  w3-border  w3-hoverable w3-hoverable w3-small w3-centered ">
    <thead>
    <tr>
    <th text-align="center" rowspan="2">Signal Name</th>
    <th colspan="3" > Signal Properties</th>
    <th colspan="2" > Configuration Parameters</th>
    </tr>


    <tr>
    <th>Message Name</th>
    <th>Length</th>
    <th>byte_order</th>
    <th>Init Value</th>
    <th>Signal Debounce</th>
    </tr>
    </thead>
    
    '''


    def html_print(sig_list,tx):
        
        temp_html_css_content=''
        temp_js=' '
        #print msg_list
        for index in sig_list:
            #decide_input_type=''
            
            #temp_js=temp_js+'document.getElementById("id_'+index['Msg_name']+'").checked = (data[0].'+index['Msg_name']+' === "on" ? true : false);\n'
            #{'GenSigInactiveValue': '0', 'DescriptionE': '', 'signal_name': 'AppTempAdjustReq_DDP', 'CommentRxJ': '', 'CommentRxE': '', 'DescriptionJ': '',
            #'Len': '8','CommentTxJ': '', 'GenSigSendType': '', 'ValueTableE': '', 'Endbit': '7', 'GenSigStartValue': '0', 'Order': 'Motorola', 'CommentTxE': ''}
            
            
            temp_html_css_content = temp_html_css_content+'''<tr id="'''+index['signal_name'].upper()+'''"><div id='''+str(index['signal_name'])+'''>\n'''+\
            '''<td><label class="w3-label w3-text-light-grey" >'''+str(index['signal_name'])+'''</label></td>\n'''+\
            '''<td><label class="w3-label w3-text-light-grey" >'''+str(index['Msg_name'])+'''</label></td>\n'''+\
            '''<td><label class="w3-label w3-text-light-grey" >'''+str(index['Len'])+'''</label></td>\n'''+\
            '''<td><label class="w3-label w3-text-light-grey" >'''+str(index['Order'])+'''</label></td>'''
            
            
            if (tx=='tx'):
                temp_html_css_content+='''<td><input class="w3-input w3-validate" id = "'''+str(index['signal_name'].upper())+'''_tx_init_value" name = "'''+str(index['signal_name'].upper())+'''_tx_init_value" value ="'''
                try:
                    temp_html_css_content+=hex(int(index['GenSigStartValue']))
                except:
                    temp_html_css_content+='0x0'
                temp_html_css_content+='''" onblur="MakeWidth(this)" ></td>'''
                
                temp_js +='if ("'+index['signal_name'].upper()+'_tx_init_value" in data)\n {\n  document.getElementById("'+str(index['signal_name'].upper())+'_tx_init_value").value = data.'+index['signal_name'].upper()+'_tx_init_value;\n}\n'
                
                check_box=['_tx_debounce']
                #drop_down=[('_tx_msg_type',['Appl','Diag','NM'])]
                
                for i in check_box:
                    temp_js=temp_js+'document.getElementById("'+index['signal_name'].upper()+i+'").checked = (data.'+index['signal_name'].upper()+i+' == "on" ? true : false);\n'
                    temp_html_css_content = temp_html_css_content+'''<td><input class="'''+i.lstrip('_')+'''" id="'''+index['signal_name'].upper()+i+'''"  name="'''+index['signal_name'].upper()+i+'''" checked="false" type="checkbox"></td>'''+'\n'
  
            else:
                
                temp_html_css_content+='''<td><input class="w3-input w3-validate" id = "'''+str(index['signal_name'].upper())+'''_rx_init_value" name = "'''+str(index['signal_name'].upper())+'''_rx_init_value" value ="'''
                try:
                    temp_html_css_content+=hex(int(index['GenSigStartValue']))
                except:
                    temp_html_css_content+='0x0'
                temp_html_css_content+='''" onblur="MakeWidth(this)" ></td>'''
                temp_js +='if ("'+index['signal_name'].upper()+'_rx_init_value"  in data)\n {\n  document.getElementById("'+str(index['signal_name'].upper())+'_rx_init_value").value = data.'+index['signal_name'].upper()+'_rx_init_value;\n}\n'
                
                check_box=['_green_drive','_signal_content']
                #drop_down=[('_tx_msg_type',['Appl','Diag','NM'])]
                
                for i in check_box:
                    temp_js=temp_js+'document.getElementById("'+index['signal_name'].upper()+i+'").checked = (data.'+index['signal_name'].upper()+i+' == "on" ? true : false);\n'
                    temp_html_css_content = temp_html_css_content+'''<td><input class="'''+i.lstrip('_')+'''" id="'''+index['signal_name'].upper()+i+'''"   name="'''+index['signal_name'].upper()+i+'''" checked="false" onclick="'''+i.lstrip('_')+'''_clicked(this)" type="checkbox"></td>'''+'\n'
                
                #Signal Fault DTC
                temp_html_css_content+='''<td><input class="w3-input" id = "'''+str(index['signal_name'].upper())+'''_signal_fault_id" name = "'''+str(index['signal_name'].upper())+'''_signal_fault_id"  onblur="MakeWidth(this)" ></td>\n'''
                temp_js +='\n if  ("'+index['signal_name'].upper()+'_signal_fault_id"  in data)\n {\n  document.getElementById("'+index['signal_name'].upper()+'''_signal_fault_id'''+'").value = data.'+index['signal_name'].upper()+'_signal_fault_id;\n}\n'
                
                drop_down_1=[('_os_notify',['No_Delay','200ms_Delay_g1','200ms_Delay_g2'])]
                for i in drop_down_1:
                    temp_html_css_content = temp_html_css_content+'''<td><select id="'''+index['signal_name'].upper()+i[0]+'''_no_of_events" style="width:100"  class="'''+str(index['signal_name'].upper())+i[0]+'''_no_of_events "  name="'''+str(index['signal_name'].upper())+i[0]+'''_no_of_events"  onchange="holder_clicked(this)" style="width:100%">'''
                    temp_js +='document.getElementById("'+index['signal_name'].upper()+i[0]+'''_no_of_events'''+'").value = data.'+index['signal_name'].upper()+i[0]+'_no_of_events;\n'
                    for no_of_event in range(len(i[1])):
                        temp_html_css_content+='<option value="'+i[1][no_of_event]+'">'+i[1][no_of_event]+'</option>\n'
            temp_html_css_content+='''</tr>\n</div>'''
                    
                    
        return (temp_html_css_content,temp_js)

    from Dbc_Parser import dbc_parser

    dbc=dbc_parser(file_name,node)
    
    
    vnim_cfg_file = open(data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
    vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
    vnim_cfg_file.close()
  
    il_msg_tx=[]
    il_msg_rx=[]
  
   
    all_message_tx = dbc.get_msg_type('ALL','tx')
    for mes in all_message_tx:
      if vnim_msg_cfg_data[mes['Msg_name']+'_tx_enable'] in ['on','ON','On',1,'1']:
        if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
          il_msg_tx.append(mes)
 
    #il_sorted_mes_tx = sorted(il_msg_tx,key = lambda x: x['Msg_name'])
  
    all_message_rx = dbc.get_msg_type(full_msg,'rx')
    for mes in all_message_rx:
      if vnim_msg_cfg_data[mes['Msg_name']+'_rx_enable'] in ['on','ON','On',1,'1']:
        if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
          il_msg_rx.append(mes)
      
    
    '''#print dbc.get_msg_type('GenMsgIlSupport','tx')[0]
    enum = dbc.get_enum_values()
    #il_tx_message=None
    il_tx_message=dbc.get_msg_type(all_parser,'tx')
    il_rx_message=dbc.get_msg_type(all_parser,'rx')
    '''
       
    il_tx_message_sorted = sorted(il_msg_tx,key = lambda x: x['Msg_name'])
    il_rx_message_sorted = sorted(il_msg_rx,key = lambda x: x['Msg_name'])
    
    for mes in il_tx_message_sorted:
        sig_par=[]
        sorted_list=[]
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            mes['Sig_List'][signals]['Msg_name']=mes['Msg_name']
            sig_par.append(mes['Sig_List'][signals])
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
        
        il=html_print(sig_sorted,'tx')
        html_css_content=html_css_content+il[0]
        js+=il[1]
    #GenSigStartValue      
        
    
    #js=js+il[1]
    
    
    #Rx Signals
    html_css_content=html_css_content+'</table><br><label class="w3-label w3-text-light-grey">\n<h1>Rx Signals</h1></label>'

    html_css_content = html_css_content+'''<table  class ="w3-table  w3-bordered  w3-border w3-hoverable">
    <table id="rx_table" style="width:100%" class ="w3-table  w3-bordered  w3-border w3-hoverable w3-small w3-centered ">
    <thead>
    <tr>
    <th text-align="center" rowspan="2">Message Name</th>
    <th colspan="3" > Signal Properties</th>
    <th colspan="5" > Configuration Parameters</th>
    </tr>
    <tr>
    <th>Message Name</th>
    <th>Length</th>
    <th>Byte_order</th>
    
    <th>Init Value</th>
    <th>Green Drive enable</th>
    <th>Signal Content Error check</th>
    <th>Signal Content Error DTC ID</th>
    <th>App notification delay</th>
    </tr>
    </thead>
    '''
    #print il_rx_message_sorted[0]
    for mes in il_rx_message_sorted:
    
        sig_par=[]
        sorted_list=[]
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            mes['Sig_List'][signals]['Msg_name']=mes['Msg_name']
            sig_par.append(mes['Sig_List'][signals])
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
        
        il=html_print(sig_sorted,'rx')
        html_css_content=html_css_content+il[0]
        js+=il[1]
        
        
  
    html_css_content = html_css_content +""" </table>
    <br>
    <br>
    <br>
    
    </form>
    </div> 
    </div> 
    </body>
    </html>
    """
    #print html_css_content
    html= open(html_dir+'CanDbcSigConfiguration.html', 'w',encoding='latin-1')
    html.write(html_css_content)
    html.close()
    #print js
    jscript = open(java_dir+'CanDbcSigConfiguration.js', 'w',encoding='latin-1')

    jscript.write(js)
    
    
    jscript.close()

if __name__ == '__main__':
    #html_sig('FF_Door.dbc','PDP')
    pass
