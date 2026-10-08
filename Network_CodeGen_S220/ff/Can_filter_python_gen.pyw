  

def html(file_name,node):
    import os
    js ='\n'
    html_dir= './html/'
    data_dir= './data/'
    java_dir = './js/'
    
    il_parser = 'GenMsgILSupport'
    nm_parser = 'NmMessage'
    tp_parser = 'NmMessage'
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
    </head>
    <body onload="load()" class="w3-container w3-grey">"""

    file1=open(html_dir+'Tool_Index_Page.html','r')
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
    <th>Buffer Allocation</th>
    <th>Messsage Type</th>
    </tr>
    '''

              

         #print Configuration_dict_map_default
         #print Configuration_dict_map_range
    #print print_order

    

    def html_print(msg_list,type,tx):
        if msg_list != None:
            temp_html_css_content=''
            temp_js=' '
            for index in msg_list:
                #print index , ': ' ,Configuration_dict_map_range[index]
                #decide_input_type=''
                if type=='NM':
                    temp_js=temp_js+'document.getElementById("id_'+index['Msg_name']+'").checked =  true ;\n'
                elif type=='DIAG':
                    temp_js=temp_js+'document.getElementById("id_'+index['Msg_name']+'").checked = true ;\n'
                else:
                    temp_js=temp_js+'document.getElementById("id_'+index['Msg_name']+'").checked = ((data[0].'+index['Msg_name']+' == "on" || data[0].'+index['Msg_name']+' == "true") ? true : false);\n'
                
                temp_html_css_content = temp_html_css_content+'''<tr width="100%">
                <td width="100/2" word-wrap"break-word" >'''
                #parse_type=[]
                #parse_type = (Configuration_dict_map_range[index]).split('..')
                temp_html_css_content = temp_html_css_content +  '<label class="w3-label w3-text-light-grey"  word-wrap="break-word">\
                '+index['Msg_name']+'</label></td>\n'
                
                if type=='NM':
                    temp_html_css_content = temp_html_css_content + '<td width="100/4">\n <input class="id_'+type+'_'+tx+'" id="id_'+index['Msg_name']+'" onclick="check_clicked(this)" checked="checked" name="'+index['Msg_name']+'" onclick="click_function()" type="checkbox"  /><lable>Full CAN</label></td>'
                elif type=='DIAG':
                    temp_html_css_content = temp_html_css_content + '<td width="100/4">\n <input class="id_'+type+'_'+tx+'" id="id_'+index['Msg_name']+'" onclick="check_clicked(this)" checked="checked" name="'+index['Msg_name']+'" onclick="click_function()" type="checkbox"  /><lable>Full CAN</label></td>'
                else:
                    temp_html_css_content = temp_html_css_content + '<td width="100/4">\n <input class="id_'+type+'_'+tx+'" id="id_'+index['Msg_name']+'" onclick="check_clicked(this)"  name="'+index['Msg_name']+'" onclick="click_function()" type="checkbox"><lable>Full CAN</label></td>'
                
                temp_html_css_content = temp_html_css_content +'<td width="100/4"><label class="w3-label w3-text-light-grey" >'+type+'</label>\
                </td>\
                </tr>'
                
                
            
            return (temp_html_css_content,temp_js)

    from Dbc_Parser import dbc_parser

    dbc=dbc_parser(file_name,node)
    #print dbc.get_msg_type(il_parser,'tx')[0]
    try:
        if html_print(dbc.get_msg_type(il_parser,'tx'),'APPL','tx') != None:
            il=html_print(dbc.get_msg_type(il_parser,'tx'),'APPL','tx')
            html_css_content=html_css_content+il[0]
            js=js+il[1]
    except:
        #raise ValueError("Please check the il attribute settings")
        pass
    try:
        if html_print(dbc.get_msg_type(nm_parser,'tx'),'NM','tx') != None:
            nm=html_print(dbc.get_msg_type(nm_parser,'tx'),'NM','tx')
            html_css_content=html_css_content+nm[0]
            js=js+nm[1]
    except:
        #raise ValueError("Please check the nm attribute settings")
        pass
    try:
        if html_print(dbc.get_msg_type(tp_parser,'tx'),'DIAG','tx')!= None:
            diag=html_print(dbc.get_msg_type(tp_parser,'tx'),'DIAG','tx')
            html_css_content=html_css_content+diag[0]
            js=js+diag[1]
    except:
        #raise ValueError("Please check the diag attribute settings")
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
    <th>Buffer Allocation</th>
    <th>Messsage Type</th>
    '''
    if html_print(dbc.get_msg_type(il_parser,'rx'),'APPL','rx')!= None:
        il=html_print(dbc.get_msg_type(il_parser,'rx'),'APPL','rx')
        html_css_content=html_css_content+il[0]
        js=js+il[1]
    
    
    #html_css_content=html_css_content+html_print(dbc.get_msg_type('NmMessage','tx'),'NM')
    if html_print(dbc.get_msg_type(tp_parser,'rx'),'DIAG','rx') != None:
        tp=html_print(dbc.get_msg_type(tp_parser,'rx'),'DIAG','rx')
        html_css_content=html_css_content+tp[0]
        js=js+tp[1]
    
     
    html_css_content = html_css_content +""" </table>
    <input type="submit" value="Save and Back" id="form_submit">
    </form>
    </div> 
    </div> 
    </body>
    </html>
    """

    #print html_css_content
    html= open(html_dir+'CanFilterconfiguration.html', 'w')
    html.write(html_css_content)
    html.close()
    #print js
    jscript = open(java_dir+'CanFilterconfiguration.js', 'w')
   
    jscript.write(js)
    
    
    jscript.close()

if __name__ == '__main__':
    #html('FF_Door.dbc','DDP')
    pass
