  

def html(file_name,node):
    import os
    js ='\n'
    html_dir= './html/'
    data_dir= './data/'
    java_dir = './js/'
    
    il_parser = 'GenMsgILSupport'
    nm_parser = 'NmMessage'
    tp_parser = 'NmMessage'
    all_parser='ALL'
    
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
    function enable_clicked(elem){
        
        var sig = elem.id;
        sig=sig.split('_enable')[0];
        if (elem.checked)
        {
            document.getElementById(sig+'_msg_type_no_of_events').disabled = false;            
        }
        else{   
            document.getElementById(sig+'_msg_type_no_of_events').disabled = true;         
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

    html_css_content = html_css_content + '<form action="BackEnd.Filter_SaveButton" id="form" data-bind="true">\n<label class="w3-label w3-text-light-grey">\
    <h1>Tx Messages</h1></label>'

    html_css_content = html_css_content+'''<table  class ="w3-table  w3-bordered  w3-border w3-hoverable">
    <thead>
    <tr>
    <th> Configurable options </th>
    <th colspan="2" text-align="center">Channel 0</th>
    </tr>
    </thead>
    <tr><th>Message Name</th>
    <th>Enable/Disable Msg</th>
    <th>Messsage Type</th>
    </tr>
    '''

    def html_print(msg_list,type,tx):
        if msg_list != None:
            temp_html_css_content=''
            temp_js=' '
            for index in msg_list:
                
                temp_html_css_content = temp_html_css_content+'''<tr width="100%">
                <td  width="33%" text-align="center" >'''
                #parse_type=[]
                #parse_type = (Configuration_dict_map_range[index]).split('..')
                temp_html_css_content = temp_html_css_content +  '<label class="w3-label w3-text-light-grey" >\
                '+index['Msg_name']+'</label></td>\n'
                
                check_box=['_enable']
                for i in check_box:
                        temp_js=temp_js+'document.getElementById("'+index['Msg_name'].upper()+i+'").checked = (data.'+index['Msg_name'].upper()+i+' == "on" ? true : false);\n'
                        temp_html_css_content = temp_html_css_content+'''<td width="33%" text-align="center"><input  class="'''+i.lstrip('_')+'''" id="'''+index['Msg_name'].upper()+i+'''"   name="'''+index['Msg_name'].upper()+i+'''" checked="false" onclick="'''+i.lstrip('_')+'''_clicked(this)"'''+'''type="checkbox"></td>'''+'\n'
                    
                drop_down=[('_msg_type',['Appl','NM','Diag'])]
                for i in drop_down:
                        temp_html_css_content = temp_html_css_content+'''<td width="33%" text-align="center" ><select  id="'''+index['Msg_name'].upper()+i[0]+'''_no_of_events" style="width:100"  class="'''+str(index['Msg_name'].upper())+i[0]+'''_no_of_events "  name="'''+str(index['Msg_name'].upper())+i[0]+'''_no_of_events"  onchange="holder_clicked(this)" style="width:100%">'''
                        temp_js +='document.getElementById("'+index['Msg_name'].upper()+i[0]+'''_no_of_events'''+'").value = data.'+index['Msg_name'].upper()+i[0]+'_no_of_events;\n'
                        for no_of_event in range(len(i[1])):
                            temp_html_css_content+='<option value="'+i[1][no_of_event]+'">'+i[1][no_of_event]+'</option>\n'
   
                temp_html_css_content+='</tr>'
                
            return (temp_html_css_content,temp_js)

    from Dbc_Parser import dbc_parser

    dbc=dbc_parser(file_name,node)
    #print dbc.get_msg_type(il_parser,'tx')[0]
    try:
        il_mes_tx=dbc.get_msg_type(il_parser,'tx')
        il_sorted_mes_tx = sorted(il_mes_tx,key = lambda x: x['Msg_name'])
        other_msg =[]
        all_msg=dbc.get_msg_type(all_parser,'tx')
        all_msg_sorted_tx = sorted(all_msg,key = lambda x: x['Msg_name'])
 
        for mes in all_msg_sorted_tx:
            if mes not in il_sorted_mes_tx:
              other_msg.append(mes)
              
        if html_print(il_sorted_mes_tx,'APPL','tx') != None:
            il=html_print(il_sorted_mes_tx,'APPL','tx')
            html_css_content=html_css_content+il[0]
            js=js+il[1]
            
        if html_print(other_msg,'APPL','tx') != None:
            il=html_print(other_msg,'APPL','tx')
            html_css_content=html_css_content+il[0]
            js=js+il[1]
    except:
        #raise ValueError("Please check the il attribute settings")
        pass
 
    

    html_css_content=html_css_content+'</table><br><label class="w3-label w3-text-light-grey">\
    <h1>Rx Messages</h1></label>'

    html_css_content = html_css_content+'''<table  class ="w3-table  w3-bordered  w3-border w3-hoverable">
    <thead>
    <tr>
    <th> Configurable options </th>
    <th colspan="2" text-align="center">Channel 0</th>
    </tr>
    </thead>
    <tr><th>Message Name</th>
    <th>Enable/Disable Msg</th>
    <th>Messsage Type</th>
    </tr>
    '''
    try:
        il_mes_rx=dbc.get_msg_type(il_parser,'rx')
        il_sorted_mes_rx = sorted(il_mes_rx,key = lambda x: x['Msg_name'])
        other_msg =[]
        all_msg=dbc.get_msg_type(all_parser,'rx')
        all_msg_sorted_rx = sorted(all_msg,key = lambda x: x['Msg_name'])
 
        for mes in all_msg_sorted_rx:
            if mes not in il_sorted_mes_rx:
              other_msg.append(mes)
              
        if html_print(il_sorted_mes_rx,'APPL','rx') != None:
            il=html_print(il_sorted_mes_rx,'APPL','rx')
            html_css_content=html_css_content+il[0]
            js=js+il[1]
            
        if html_print(other_msg,'APPL','rx') != None:
            il=html_print(other_msg,'APPL','rx')
            html_css_content=html_css_content+il[0]
            js=js+il[1]
    except:
        #raise ValueError("Please check the il attribute settings")
        pass
    
     
    html_css_content = html_css_content +""" </table>
    <input type="submit" value="Save and Back" id="form_submit">
    </form>
    </div> 
    </div> 
    </body>
    </html>
    """

    #print html_css_content
    html= open(html_dir+'CanFilterconfiguration.html', 'w',encoding='latin-1')
    html.write(html_css_content)
    html.close()
    #print js
    jscript = open(java_dir+'CanFilterconfiguration.js', 'w',encoding='latin-1')
   
    jscript.write(js)
    
    
    jscript.close()

if __name__ == '__main__':
    #html('FF_Door.dbc','DDP')
    pass
