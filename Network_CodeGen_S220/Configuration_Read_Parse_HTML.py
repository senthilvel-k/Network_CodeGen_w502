
import xlrd




def config_generator(Layer):
    html_dir='./html/'
    js_dir='./js/'
    data_dir='./data'

    wb = xlrd.open_workbook('Candriver_config.xls')
    read_msg_lst_sheet_tx = wb.sheet_by_name(Layer)

    print_order = []

    Num_of_Columns= read_msg_lst_sheet_tx.ncols
    Num_Config = Num_of_Columns / 4
    #printNum_Config

    def for_loop_nesitng(Num_dependencies , Crrent_iterate_dependency,iterate_name):
                    if iterate_name != 'Configuration Name' and iterate_name !='':
                        what_symbol = ''
                        Identify_dependency=''
                        
                        iterate_list=[]
                        #dependency name eg:For-x-CAN_CFG_NUMBER_OF_CONTROLLERS
                        #Identify_dependency=CAN_CFG_NUMBER_OF_CONTROLLERS
                        #what_symbol = x
                        Identify_dependency = split_ups[(Crrent_iterate_dependency+1)*2]
                        what_symbol = split_ups[(Crrent_iterate_dependency*2)+1]
                        
                        iterate_list = (iterate_name).split(what_symbol)
                        #print iterate_list,'1st'
                        for j in range(0, len(Identify_dependency.split(what_symbol))):
                            if len( Identify_dependency.split(what_symbol))>1:
                                Identify_dependency = Identify_dependency.split(what_symbol)[0]+str(j)+Identify_dependency.split(what_symbol)[1]
                                ##printhello
                            #print what_symbol,'2nd'
                            #print Identify_dependency,'3rd'
                            for x in range(0, int(Configuration_dict_map_default[Identify_dependency])):
                           
                                iterate_name =  iterate_list[0]+str(x)+iterate_list[1]
                                #printiterate_name
                                if (Crrent_iterate_dependency < (Num_dependencies -1)):
                                    for_loop_nesitng(Num_dependencies , Crrent_iterate_dependency+1,iterate_name)
                                else:
                                    try:
                                        if iterate_name in Configuration_dict_map_range.keys():
                                            pass
                                        else:
                                            print_order.append(iterate_name)                                
                                        Configuration_dict_map_range[iterate_name]=(read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index+1) .value)
                                        Configuration_dict_map_default[iterate_name]=(read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index+2).value)
                                        Configuration_dict_map_description[iterate_name]=(read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index+3).value)
                                    except:
                                        pass



    '''main'''
    col_index=0
    Configuration_dict_map_range={}
    Configuration_dict_map_default={}
    Configuration_dict_map_description={}
    #Num_Config - no of cofig for each configuration eg:generic config ,channel based config  
    #each group heading has 4 items
    for config_index in range(0,Num_Config):
         split_ups=[]
         Num_dependencies=0

         loop_counts =[]
         start_index = 0  
         col_index = config_index*4
         for r in range(0,read_msg_lst_sheet_tx.nrows):
             if (read_msg_lst_sheet_tx .cell(rowx=0,colx=col_index).value =='One_time_Configuration'):
                 if (read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index).value!='' and read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index).value!='One_time_Configuration' and read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index).value!='Configuration name'):
                     Configuration_dict_map_range[read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index).value]=(read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index+1) .value)
                     Configuration_dict_map_default[read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index).value]=(read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index+2).value)
                     Configuration_dict_map_description[read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index).value]=(read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index+3).value)

                     print_order.append(read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index).value) 
             else:
                start_index=2
                
                loop_counts =[]
                split_ups = (read_msg_lst_sheet_tx .cell(rowx=0,colx=col_index).value).split('-')
                ##printsplit_ups
                Num_dependencies = (len(split_ups)-1)/2
                
                iterate_name=''
                iterate_name = (read_msg_lst_sheet_tx .cell(rowx=r,colx=col_index).value)
                if len(iterate_name.split('For-')) ==1:
                    for_loop_nesitng(Num_dependencies , 0,iterate_name)

                      

    html_css_content="""
    <!DOCTYPE html>
    <html>
    <head>
    <title>"""+Layer+"""</title>
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

    file1=open('.\html\Tool_Index_Page.html','r')
    start=0
    for line in file1.readlines():
        if '<!--copy_start-->' == line.rstrip('\n'):
            start=1
        elif '<!--copy_end-->' == line.rstrip('\n'):
            start=0
        if start == 1:
            html_css_content=html_css_content+line

    file1.close()

    html_css_content = html_css_content + '<form action="BackEnd.'+Layer+'_SaveButton" id="form" data-bind="true">\n'
    html_css_content = html_css_content+'''<table  class ="w3-table  w3-bordered  w3-border w3-hoverable">
    <thead>
    <tr>
    <th> Configurable options </th>
    <th>Channel 0</th>
    </tr>
    </thead>'''

              

         #print Configuration_dict_map_default
         #print Configuration_dict_map_range
    #print print_order

    #print Configuration_dict_map_default
    js=''


    for index in  print_order:
        #print index , ': ' ,Configuration_dict_map_range[index]
        decide_input_type=''
        js=js+'document.getElementById("'+index+'").value = data[0].'+index+';\n'
        html_css_content = html_css_content+'''<tr>
    <td>'''
        parse_type=[]
        parse_type = (Configuration_dict_map_range[index]).split('..')
        html_css_content = html_css_content +  '<label class="w3-label w3-text-light-grey" onclick="accordionfn(\''+index+'_ACC\')" ><b>'+index+'</b></label><Br>\n\
      <div id="'+index+'_ACC" class="w3-accordion-content w3-animate-left "style="width:100%">\
      <BR>\
      <Div>\n\
    <p class="w3-container w3-text-light-grey  w3-border-blue-grey ">'+Configuration_dict_map_description[index]+'</p>\
    </div>\
    </div>\
    </td>\
    <td>\n'
        if(len(parse_type)>1):
            pass
            js=js+index+'validate();\n'
            html_css_content = html_css_content + '<input class="w3-input w3-validate " onblur=" '+index+'validate()" style="width:30%" value="'+ str(Configuration_dict_map_default[index]).rstrip('.')[0] +'" type="number" name="'+index+'"  id="'+index+'" min='+str(parse_type[0])+' max='+str(parse_type[1])+'><Br>\n'
            html_css_content = html_css_content +'<script>\n\
    function '+index+'validate() {\n\
    var x = document.getElementById("'+index+'");\n\
    if( x.value <'+str(parse_type[0])+'  || x.value > '+str(parse_type[1])+')\n\
    { document.getElementById("'+index+'").style.background="red";\n\
    }\n\
    else{\n\
    document.getElementById("'+index+'").style.background="white";\n\
    }\n\
    }\n\
    </script>\n'
        parse_type = (Configuration_dict_map_range[index]).split('[')
        if(len(parse_type)>1):
            parse_type = (parse_type[1]).split(']')
            #print parse_type
            parse_type = parse_type[0].split(',')
            html_css_content = html_css_content + '<select id="'+index+'" class="w3-select " name="'+index+'"  id="'+index+'"style="width:40%"><Br>\n'
            for options in parse_type:
                html_css_content = html_css_content + '<option value="'+options+'">'+options+'</option>\n'
            html_css_content = html_css_content + '</select><Br><Br>\n'
        
        parse_type =(Configuration_dict_map_range[index]).split('***')
        if(len(parse_type)>1):
            parse_type = (parse_type[1])
            html_css_content = html_css_content + '<input  type ="text" id="'+index+'" class="w3-input w3-border" value="'+parse_type+'"name="'+index+'"  id="'+index+'"style="width:40%"><Br>\n'
            
        html_css_content = html_css_content+'</td>\n</tr>\n'
    html_css_content = html_css_content +""" </table>
    <br><input type="submit" value="Save and Back" id="form_submit">
    </form>
    </div> 
    </div> 
    </body>
    </html>
    """

    #print html_css_content
    html= open(html_dir+'Can'+Layer+'Configuration.html', 'w')
    html.write(html_css_content)
    html.close()
    #print js
    jscript = open(js_dir+'Can'+Layer+'Configuration.js', 'w')
    jscript.write(js)
    jscript.close()

if __name__ == "__main__":
    sheet_layer = ['DRV','DISP','IL','VNIM','NM','TP','DIAG']
    for val in sheet_layer:
        config_generator(val)
