from db_cm import UseDatabase
from rich.console import Console
from rich.table import Table
from rich.text import Text
import argparse


config_database = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'database': 'todo'
}


def command_arguments():
    parser = argparse.ArgumentParser(description="Todo app")
    parser.add_argument('-s', '--show', help="shows todo tasks", action='store_true')
    parser.add_argument('-r', '--remove', help="remove task", nargs=1, type=int)
    parser.add_argument('-a', '--add', help="add task", nargs=1, type=str )
    parser.add_argument('-c', '--change', help="change status task", nargs=1, type=int)
    args = parser.parse_args()
    return args


def show_tasks():
    with UseDatabase(config_database) as cursor:
        SQL = "SELECT id, task_name, task_status FROM tasks;"
        cursor.execute(SQL)
        result = cursor.fetchall()
        return result


def remove_task(task_id):
    with UseDatabase(config_database) as cursor:
        SQL = "DELETE FROM tasks WHERE id=%s;"
        cursor.execute(SQL, (task_id, ))


def add_task(task_name):
    task_status = "\u274C"
    with UseDatabase(config_database) as cursor:
        SQL = "INSERT INTO tasks (task_name, task_status) VALUES (%s, %s)"
        cursor.execute(SQL, (task_name, task_status))


def change_status_task(task_id):
    with UseDatabase(config_database) as cursor:
        SQL = "SELECT task_status FROM tasks WHERE id=%s"
        cursor.execute(SQL, (task_id, ))
        icon = cursor.fetchone()
        icon = icon[0]

        task_status = "\u2705"

        if icon == "\u2705":
            task_status = "\u274C"
        elif icon == "\u274C":
            task_status = "\u2705"

        SQL = "UPDATE tasks SET task_status=%s WHERE id=%s"
        cursor.execute(SQL, (task_status, task_id))


def draw_table(tasks: list):
    table = Table()

    table.add_column("ID", style="cyan")
    table.add_column("TASK NAME", style="magenta")
    table.add_column("TASK STATUS", style="green")
    
    for row in tasks:
        text = None
        if row[2] == "\u2705":
            text = Text(row[2])
            text.stylize("bold green")
        elif row[2] == "\u274C":
            text = Text(row[2])
            text.stylize("bold red")

        table.add_row(str(row[0]), row[1], text)

    console = Console()
    console.print(table)


def main():
    args = command_arguments()
    if args.show:
        draw_table(show_tasks())
    if args.remove:
        remove_task(args.remove[0])
    if args.add:
        add_task(args.add[0])
    if args.change:
        change_status_task(args.change[0])
    

if __name__ == '__main__':
    main()