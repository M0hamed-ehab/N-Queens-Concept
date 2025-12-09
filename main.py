import flet as ft
from classes.board import Board
import time
import functional
import imperative

############################################################--GUI--#############################################################
#To run write python main.py in terminal but please make sure you installed flet by putting "pip install flet" in terminal/cmd
def main(page: ft.Page):
    page.title = "N-Queens Problem"
    page.adaptive=True
    page.appbar = ft.AppBar(
        title = ft.Text(value="N-Queens", color="green", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        center_title=True,)
    # page.window.width = 600
    # page.window.height = 700
    page.auto_scroll = True
    page.scroll= "ALWAYS"

    def show_green(r, c, result):
        n = int(Ntiles.value)
        green = set()

        for i in range(n):
            green.add((r, i)) 
            green.add((i, c)) 

        for i in range(n):
            for j in range(n):
                if abs(r - i) == abs(c - j):
                    green.add((i, j))


        columns = [ft.DataColumn(ft.Text("")) for _ in range(n)]
        rows = []
        for i in range(n):
            cells = []
            for j in range(n):

                if (i, j) in green:
                    if result[i][j] == 1:
                        cells.append(ft.DataCell(ft.Image(src="icons/4LG.png",fit=ft.ImageFit.CONTAIN, width=24,height=24), on_tap=lambda e, r=i, c=j: show_green(r, c, result)))
                    else:
                        cells.append(ft.DataCell(ft.Icon(name=ft.Icons.CLOSE_ROUNDED, color=ft.Colors.LIGHT_GREEN)))
                else:
                    if result[i][j] == 1:
                        cells.append(ft.DataCell(ft.Image(src="icons/4G.png",fit=ft.ImageFit.CONTAIN, width=24,height=24), on_tap=lambda e, r=i, c=j: show_green(r, c, result)))
                    else:
                        cells.append(ft.DataCell(ft.Text(str(" "))))

            rows.append(ft.DataRow(cells=cells))

        table = ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(3, ft.Colors.WHITE),
            border_radius=10,
            heading_row_height=0,
            vertical_lines=ft.border.BorderSide(3, ft.Colors.WHITE),
            horizontal_lines=ft.border.BorderSide(3, ft.Colors.WHITE),
            expand=True
        )
        table_container = ft.Container(
            content=ft.Row(
                controls=[table],
                scroll=ft.ScrollMode.ALWAYS,
            ),
            expand=True,
            padding=10,
        )
        output_container.content = table_container
        page.update()


    def show_table(result,comp=False):
        columns = [ft.DataColumn(ft.Text("")) for _ in range(int(Ntiles.value))]
        rows = []
        

        
        for r, row_data in enumerate(result):
            cells = []
            for c, cell in enumerate(row_data):
                if cell == 1:
                    if comp:
                        cells.append(ft.DataCell(ft.Image(src="icons/4G.png",fit=ft.ImageFit.CONTAIN, width=24,height=24)))
                    else:
                        cells.append(ft.DataCell(ft.Image(src="icons/4G.png",fit=ft.ImageFit.CONTAIN, width=24,height=24), on_tap=lambda e, r=r, c=c: show_green(r, c, result)))
                else:
                    cells.append(ft.DataCell(ft.Text(str(" "))))
            rows.append(ft.DataRow(cells=cells))

        table = ft.DataTable(columns=columns, rows=rows, border=ft.border.all(3, ft.Colors.WHITE), border_radius=10, heading_row_height=0,
            vertical_lines=ft.border.BorderSide(3, ft.Colors.WHITE), horizontal_lines=ft.border.BorderSide(3, ft.Colors.WHITE),)
        
        table_container = ft.Container(
            content=ft.Row(
                controls=[table],
                scroll=ft.ScrollMode.ALWAYS, 
            ),
            expand=True,
            padding=10,
        )
        return table_container

    def validation():
        if not Ntiles.value.isdigit() or int(Ntiles.value)<=0:
            output_text.value = "Please enter a valid positive integer for number of tiles."
            output_container.content = output_text
            output_time.value = ""
            page.update()
            return
        if color_dropdown.value is None:
            output_text.value = "Please select a paradigm."
            output_container.content = output_text
            output_time.value = ""
            page.update()
            return



    def button_clicked(e):
        validation()
        result, timing = solve(int(Ntiles.value), int(color_dropdown.value))
        if isinstance(result, list):
            

            
            output_container.content = show_table(result)
        else:
            output_text.value = result
            output_container.content = output_text
        output_time.value = f"Time taken: {timing:.6f} seconds"
        page.update()

    def all_Clicked(e):
        validation()
        page.all_results=[]
        solve_all(int(Ntiles.value))
        page.update()

    def show_comp():
        columns=[
            ft.DataColumn(ft.Text("Paradigm")),
            ft.DataColumn(ft.Text("Time Taken (seconds)")),
        ]
        rows=[]
        for name,t, timing in page.all_results:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(ft.Text(f"{timing:.6f}"))
                    ]
                )
            )
        table=ft.DataTable(columns=columns, rows=rows, border=ft.border.all(1, ft.Colors.WHITE), border_radius=10)

        content=ft.Column(
            [
                ft.Text("Comparison of Paradigms", weight=ft.FontWeight.BOLD, size=18, text_align=ft.TextAlign.CENTER),
                table,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        compall=ft.AlertDialog(
            modal=True,
            title="N-Queens Comparison",
            content=content,
            alignment=ft.alignment.center,
            actions=[
                ft.ElevatedButton("Close",bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE,on_click=lambda e: page.close(compall))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(compall)


    def solve_all(n):
        page.all_results=[]
        
        for al in range(1,3):
            x=""
            match al:
                case 1: x="Pure Functional Paradigm"
                case 2: x="Imperative Paradigm"

                
            result, timing=solve(int(n), al)
            page.all_results.append((x,result,timing))

        open_new(int(n), 1)
     

    def open_new(n, algo):
        
        
        if algo> 2:
            show_comp()
            return
        
        x,result,timing=page.all_results[algo-1]


        if isinstance(result, list):
            table = show_table(result,comp=True)
            content=ft.Column(
                    [
                        ft.Text(value=x, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        table,
                        ft.Text(f"Time taken: {timing:.6f} seconds")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
        else:
            content=ft.Column(
                    [
                        ft.Text(value=x, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text(result),
                        ft.Text(f"Time taken: {timing:.6f} seconds")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )


        new_page=ft.AlertDialog(
        modal=True,
        title = "N-Queens Solution",
        content=content,
        alignment=ft.alignment.center,
        actions=[],
        actions_alignment=ft.MainAxisAlignment.END,
        scrollable=True,
        )

        def next(e):
            page.close(new_page)
            open_new(n, algo+1)
                    

        new_page.actions=[ft.ElevatedButton("Next", on_click=next, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)]

        page.open(new_page)
            

    
    output_text = ft.Text()
    output_time = ft.Text()
    output_container = ft.Container(content=output_text, alignment=ft.alignment.center, expand=True)
    submit_btn = ft.ElevatedButton(text="Solve", on_click=button_clicked, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
    color_dropdown = ft.Dropdown(
        text_align=ft.TextAlign.CENTER,
        hint_text="Select Paradigm",
        options=[
            ft.dropdown.Option(1,"Pure Functional Paradigm"),
            ft.dropdown.Option(2,"Imperative Paradigm"),

        ],
    )

    Ntiles = ft.TextField(hint_text="Enter Number of tiles", width=200, text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
    all_btn = ft.ElevatedButton(text="All?", on_click=all_Clicked, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)

    page.add(
        ft.Container(
            content=ft.SafeArea(
                ft.Column(
                    [
                       ft.Row([Ntiles, all_btn], alignment=ft.MainAxisAlignment.CENTER ),
                        color_dropdown,
                        submit_btn,
                        output_container,
                        output_time
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS
                )
            ),
            expand=True,
            alignment=ft.alignment.center,
            
            # padding=ft.padding.only(top=-48)
        ),

        )
    



###############################################################################################################################

###########################################################--Main--############################################################

#create board & row fun
def create_row(n, acc=None):
    if acc is None:
        acc = ()
    if len(acc) == n:
        return acc
    return create_row(n, acc + (0,))

def create_board(n, acc=None):
    if acc is None:
        acc = ()
    if len(acc) == n:
        return acc
    return create_board(n, acc + (create_row(n),))

def solve(N,C):
    start_time = time.time()

    board = Board(N)
    match C:
        case 1:
            empty_board = create_board(N)
            result, found = functional.backtrack_functional(empty_board)
            elapsed = time.time() - start_time
            result_list = [list(i) for i in result]
            if found:
                return result_list, elapsed
            else:
                return "No Solution Found", elapsed
        case 2:
            imperative.backtrack_imperative(board)
        case _:
            return("No Such Search Algorithm"),0
    # return print_board(board)
    return board.print_board()

ft.app(main)

# N = int(input("\nEnter N\n"))
# C =int(input("Choose Search Algorithm Number:\n1.Backtracking Search Algorithm\n2.Best-First Search\n3.Hill-Climbing Search\n4.Cultural Algorithm\n"))
# solve(N,C)

###############################################################################################################################
