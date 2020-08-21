import networkx as nx
import matplotlib.pyplot as plt
import xlrd
import csv

#this method parses through the master list of groups and pages, organizing them in a dictionary
def StorePageInfo():
    workbook = xlrd.open_workbook('FB-pages-groups.xls')
    print(workbook)
    sheet_names = workbook.sheet_names()

    print('Sheet Names', sheet_names)

    pages_dictionary = {}

    for sheet in sheet_names:
        if 'Master List' in sheet:
            #print("HERE")
            xl_sheet = workbook.sheet_by_name(sheet)
            num_cols = xl_sheet.ncols   # Number of columns
            for row_idx in range(0, xl_sheet.nrows):    # Iterate through rows
                #print ('-'*40)
                #print ('Row: %s' % row_idx)   # Print row number
                for col_idx in range(0, num_cols):  # Iterate through columns
                    cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
                    #print("CELL", cell_obj)
                    if col_idx == 0 and row_idx > 0:
                        info = {}
                        info['type'] = xl_sheet.cell(row_idx, col_idx+1)
                        info['accesibility'] = xl_sheet.cell(row_idx, col_idx+2)
                        info['platform'] = xl_sheet.cell(row_idx, col_idx+3)
                        info['link'] = xl_sheet.cell(row_idx, col_idx+4)
                        info['followers'] = xl_sheet.cell(row_idx, col_idx+5)
                        info['description'] = xl_sheet.cell(row_idx, col_idx+6)
                        info['comments'] = xl_sheet.cell(row_idx, col_idx+7)
                        pages_dictionary[str(cell_obj)] = info


#G -- graph
# page_name -- row of page names
# content -- row of content type
# strat -- row of strategy
# calls -- row of calls to  
# this method makes the nodes for Tarun.csv and Shambhavi.csv
def MakeSocialNetwork(G, attr, filename, page_name, content, strat, calls):

    with open(filename) as csv_file:
        readCSV = csv.reader(csv_file, delimiter=',')
        for row in readCSV:
            #goal of all this is to map each type of content to its type of occurence
            if "Page/Account/Group" in row:
                continue
            if "page" in row:
                continue
            if row[page_name] == "":
                continue
            if row[page_name].lower() in G.nodes():
                if row[page_name].lower() in attr:
                    #print(row[page_name])
                    if '-' not in row[content]:
                        if row[content] not in attr[row[page_name].lower()]:
                            attr[row[page_name].lower()][row[content]] = 1
                        else:
                            attr[row[page_name].lower()][row[content]] += 1
                    if '-' not in row[strat]:
                        row_list = row[strat].replace(' ', '').replace('?', '').split(",")
                        for item in row_list:
                            if item == '':
                                continue
                            if item not in attr[row[page_name].lower()]:
                                attr[row[page_name].lower()][row[strat]] = 1
                            else:
                                attr[row[page_name].lower()][item] += 1
                    if '-' not in row[calls]:
                        row_list = row[calls].replace(' ', '').replace('?', '').split(",")
                        for item in row_list:
                            if item == '': #dont consider 
                                continue
                            if item not in attr[row[page_name].lower()] and item != ' ':
                                attr[row[page_name].lower()][row[calls]] = 1
                            else:
                                attr[row[page_name].lower()][item] += 1
                else:
                    #G.add_node(row[page_name].lower())
                    if '-' not in row[content]:
                        row_list = row[content].replace(' ', '').replace('?', '').split(",")
                        #print("ROW LIST", row_list)
                        for item in row_list:
                            if item != '':
                                attr[row[page_name].lower()][row[content]] = 1
                    if '-' not in row[strat]:
                        row_list = row[strat].replace(' ', '').replace('?', '').split(",")
                        #print("ROW LIST", row_list)
                        for item in row_list:
                            if item != '':
                                attr[row[page_name].lower()][row[strat]] = 1
                    if '-' not in row[calls]:
                        row_list = row[calls].replace(' ', '').replace('?', '').split(",")
                        #print("ROW LIST", row_list)
                        for item in row_list:
                            if item != '':
                                attr[row[page_name].lower()][row[calls]] = 1
            else:
                G.add_node(row[page_name].lower())
                if '-' not in row[content]:
                    attr[row[page_name].lower()] = {row[content]:1}
                if '-' not in row[strat]:
                    attr[row[page_name].lower()][row[strat]] = 1
                if '-' not in row[calls]:
                        attr[row[page_name].lower()][row[calls]] = 1
    return G, attr


#this makes the nodes from sana's workbook
def AddSanaWorkbook(G, attr):
    workbook = xlrd.open_workbook('Sana-Observation-Workbook.xlsx')
    print(workbook)
    sheet_names = workbook.sheet_names()

    print('Sheet Names', sheet_names)
    for sheet in sheet_names:
        if "Sheet" in sheet:
            print("SHEET OR PAYAL====================", sheet)
            continue
        if "Payal" in sheet:
            print("SHEET OR PAYAL====================", sheet)
            continue
        else:
            #make group name the key
            G.add_node(sheet)
            attr[sheet] = {}
            xl_sheet = workbook.sheet_by_name(sheet)
            num_cols = xl_sheet.ncols   # Number of columns
            #print("NUM COLS===============================\n", num_cols)
            for row_idx in range(1, xl_sheet.nrows):    # Iterate through rows
                #print ('-'*40)
                #print ('Row: %s' % row_idx)   # Print row number
                for col_idx in range(0, num_cols):  # Iterate through columns
                    cell_obj = str(xl_sheet.cell(row_idx, col_idx).value)  # Get cell object by row, col
                    #print("COL IND============================", type(col_idx))
                    if col_idx==int(5):
                        #print('content')
                        #print("CELL OBJ", cell_obj)
                        if '-' not in cell_obj:
                            row_list = cell_obj.replace(' ', '').replace('?', '').split(",")
                            for item in row_list:
                                if item not in attr[sheet]:
                                    if item != '':
                                        attr[sheet][item] = 1
                                else:
                                    attr[sheet][item] += 1
                    if col_idx == 6:
                        row_list = cell_obj.replace(' ', '').replace('?', '').split(',')
                        #print(row_list)
                        #print("CELL OBJ", cell_obj)
                        for item in row_list:
                            if '-' not in cell_obj:
                                if item not in attr[sheet]:
                                    if item != '':
                                        attr[sheet][item] = 1
                                else:
                                    attr[sheet][item] += 1
                    if col_idx == 7:
                        #print("CELL OBJ", cell_obj)
                        row_list = cell_obj.replace(' ', '').replace('?', '').split(",")
                        for item in row_list:
                            if '-' not in cell_obj:
                                if item not in attr[sheet]:
                                    if item != '':
                                        attr[sheet][item] = 1
                                else:
                                    attr[sheet][item] += 1

                        
    return G, attr

#makes the edges between nodes
def MakeEdges(G, attr):
    overlap_list = {}
    for page, types in attr.items():
        for page2, types2 in attr.items():
            #if we are looking at the same page
            if page == page2:
                continue
            else:
                for content in types:
                    for content2 in types2:
                        if content == content2:
                            overlap = min(types[content], types2[content2])
                        else:
                            continue
                        if (page2, page, content) in overlap_list:
                            continue
                        else:
                            if "A" in content:
                                if overlap > 15:
                                    overlap_list[(page, page2, content)] = overlap
                                    G.add_edge(page, page2, content_type=content, weight=overlap)
                            elif overlap > 30:
                                overlap_list[(page, page2, content)] = overlap
                                G.add_edge(page, page2, content_type=content, weight=overlap)

    #write overlap to a file
    totals = {}
    with open('overlap.txt', 'w+') as filetowrite:
        count = 1
        for k in sorted(overlap_list, key=overlap_list.get, reverse=True):
            #print(k, overlap_list[k])
            if k[2] not in totals.keys():
                totals[k[2]] = overlap_list[k]
            else:
                totals[k[2]] += overlap_list[k]
            string = str(count) + ". Pages: " + k[0] + " and " + k[1] + "\nContent Type: "+ k[2] + " with overlap: "+ str(overlap_list[k]) + "\n\n"
            filetowrite.write(string)
            count += 1
    print("TOTALS==========",{k:v for k, v in sorted(totals.items(), key=lambda item: item[1])})

def draw_graphs(G, edges, color):
    pos = nx.spring_layout(G)
    plt.figure()
    #print(edges)
    weights = [G[u][v][key]['weight']*0.015 for u,v in edges for key in G[u][v]]
    #print(weights)
    nx.draw(G, pos, node_color=color, edge_weights=weights, font_size=9, node_size=50)
    #nx.draw(G, pos, node_color=color, font_size=9, node_size=50, connectionstyle='arc3, rad = 0.1', edge_labels=dict([((u,v,),d['content_type']) for u,v,d in G.edges(data=True)]))
    edge_labels = nx.get_edge_attributes(G,'content_type')
    print(edge_labels)
    #nx.draw_networkx_edge_labels(G, pos=pos, font_color='red')
    nx.draw_networkx_edge_labels(G, pos=pos, font_size=4)
    plt.show()


def main():
    G = nx.Graph()
    attr = {}
    G, attr = MakeSocialNetwork(G, attr, 'tarun-pages.csv', 16, 4, 5, 6)
    G, attr = MakeSocialNetwork(G, attr, 'Recording-Observations-Shambhavi.csv', 0, 5, 6 , 7)
    G, attr = AddSanaWorkbook(G, attr)
    nx.set_node_attributes(G, attr)
    with open('content_count.txt', 'w+') as filetowrite:
        for page, instances in attr.items():
            string = "Page: " + page + "has content types: "
            for content, number in instances.items():
                string += " " + content + ":" + str(number) + " "
            filetowrite.write(string + "\n")

    print(attr)
    MakeEdges(G, attr)
    edges = G.edges()
    S_edges = []
    C_edges = []
    A_edges = []
    for u,v in edges:
        #print(G[u][v])
        for keys in G[u][v]:
            content = G[u][v][keys]
            #print("content=======", content)
            if 'S' in content:
                S_edges.append((u,v))
            elif 'C' in content:
                C_edges.append((u,v))
            elif 'A' in content:
                A_edges.append((u,v))
    #print("S EDGES================", S_edges)
    #print("C EDGES=================", C_edges)
    #print("A_edges=================", A_edges)
    S_subgraph = G.edge_subgraph(S_edges).copy()
    C_subgraph = G.edge_subgraph(C_edges).copy()
    A_subgraph = G.edge_subgraph(A_edges).copy()
    draw_graphs(G, edges, 'g')
    draw_graphs(S_subgraph, S_subgraph.edges(), 'b')
    draw_graphs(C_subgraph, C_subgraph.edges(), 'r')
    draw_graphs(A_subgraph, A_subgraph.edges(), 'y')


main()



