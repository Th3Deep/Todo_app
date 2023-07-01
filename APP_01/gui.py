import functions
import PySimpleGUI as sg
import time

sg.theme("Black")
# sg.theme_previewer() [it shows all themes you can apply]

clock = sg.Text('', key="Clock")
label = sg.Text("Type in a to-do")
input_box = sg.InputText(tooltip="Enter todo", key="todo")
add_button = sg.Button(image_source="add.png", key="Add", mouseover_colors="LightBlue",
                       tooltip="Add todo")

list_box = sg.Listbox(values=functions.get_todos(), key='todos',
                      enable_events=True, size=(45, 10))

edit_button = sg.Button(size=1, image_source="edit.png", key="Edit")
complete_button = sg.Button(image_source="complete.png", key="Complete")
exit_button = sg.Button(image_source="off.png", key='Exit')

window = sg.Window("My To-Do App",
                   layout=[[clock],
                           [label],
                           [input_box, add_button],
                           [edit_button, complete_button],
                           [list_box],
                           [exit_button]],
                   font=('Helvetica', 12))

while True:
    event, values = window.read(timeout=200)  # it runs every ten milliseconds the loop
    window['Clock'].update(value=time.strftime("%b %d, %Y %H:%M:%S"))
    print(event)
    print(values)
    print(values['todos'])
    match event:
        case "Add":
            todos = functions.get_todos()
            new_todo = values['todo'] + "\n"
            todos.append(new_todo)
            functions.write_todos(todos)

            window['todos'].update(values=todos)

        case "Edit":
            try:
                todo_to_edit = values["todos"][0]
                new_todo = values['todo'] + '\n'

                todos = functions.get_todos()
                index = todos.index(todo_to_edit)
                todos[index] = new_todo
                functions.write_todos(todos)
                window['todos'].update(values=todos)
            except IndexError:
                sg.popup("Select an item first", font=("Helvetica", 12))

        case "Complete":
            try:
                todo_to_complete = values["todos"][0]
                todos = functions.get_todos()
                todos.remove(todo_to_complete)
                functions.write_todos(todos)
                window['todos'].update(values=todos)
                window['todo'].update(value='')
            except IndexError:
                sg.popup("Select an item first", font=("Helvetica", 12))
        case "todos":
            try:
                window['todo'].update(value=values['todos'][0])
            except IndexError:
                sg.popup("The list has no items, try adding one", font=("Helvetica", 12))

        case 'Exit':
            sg.popup_yes_no("You want to leave?")
            break
        case sg.WIN_CLOSED:
            break

window.close()
