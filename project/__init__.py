from .src import MainWindow, data_distributor

main_window = MainWindow()

def data_distributor_loop():
    data_distributor.update()
    main_window.after(
        1000 // 60, data_distributor_loop
    )

def run():
    main_window.after(
        1000 // 60, data_distributor_loop
    )
    main_window.mainloop()

