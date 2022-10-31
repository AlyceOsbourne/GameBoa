from .src import MainWindow, data_distributor

main_window = MainWindow()

def dd_update():
    data_distributor.update()
    main_window.after(
        1000 // 60, dd_update
    )

def run():
    main_window.after(
        1000 // 60, dd_update
    )
    main_window.mainloop()

