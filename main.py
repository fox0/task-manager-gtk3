import os
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

result = {}
for pid in os.listdir('/proc/'):
    if not pid.isdigit():
        continue
    name, rss, swap = None, None, None
    for line in open('/proc/{}/status'.format(pid)).readlines():
        k, v = line.split('\t', maxsplit=1)
        if k == 'Name:':
            name = v.strip()
        elif k == 'VmRSS:':
            rss = int(v.strip().split()[0]) / 1024  # MB
        elif k == 'VmSwap:':
            swap = int(v.strip().split()[0]) / 1024  # MB
    if rss is None:
        continue
    if name in result:
        result[name] += (rss, swap)
    else:
        result[name] = (rss, swap)

software_list = [(k, v[0], v[1]) for k, v in result.items()]
software_list.sort(key=lambda x: -x[1])


class TreeViewFilterWindow(Gtk.Window):
    COLUMN_TYPES = (str, int, int)
    COLUMN_TITLE = ('name', 'rss', 'swap')

    def __init__(self):
        super().__init__(title='Процессы')
        self.connect('destroy', Gtk.main_quit)

        # self.set_border_width(10)
        self.set_default_size(300, 600)

        # Setting up the self.grid in which the elements are to be positioned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # Creating the ListStore model
        self.store = Gtk.ListStore(*self.COLUMN_TYPES)
        for i in software_list:
            self.store.append(i)
        # self.current_filter_language = None

        # # Creating the filter, feeding it with the liststore model
        # self.language_filter = self.software_liststore.filter_new()
        # # setting the filter function, note that we're not using the
        # self.language_filter.set_visible_func(self.language_filter_func)

        # creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView(
            # model=self.language_filter
            model=self.store
        )
        for i, column_title in enumerate(self.COLUMN_TITLE):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # # creating buttons to filter by programming language, and setting up their events
        # self.buttons = list()
        # for prog_language in ["Java", "C", "C++", "Python", "None"]:
        #     button = Gtk.Button(label=prog_language)
        #     self.buttons.append(button)
        #     button.connect("clicked", self.on_selection_button_clicked)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        # self.grid.attach_next_to(
        #     self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1
        # )
        # for i, button in enumerate(self.buttons[1:]):
        #     self.grid.attach_next_to(
        #         button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1
        #     )

        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    # def language_filter_func(self, model, iter, data):
    #     """Tests if the language in the row is the one in the filter"""
    #     if (
    #             self.current_filter_language is None
    #             or self.current_filter_language == "None"
    #     ):
    #         return True
    #     else:
    #         return model[iter][2] == self.current_filter_language
    #
    # def on_selection_button_clicked(self, widget):
    #     """Called on any of the button clicks"""
    #     # we set the current language filter to the button's label
    #     self.current_filter_language = widget.get_label()
    #     print("%s language selected!" % self.current_filter_language)
    #     # we update the filter, which updates in turn the view
    #     self.language_filter.refilter()


if __name__ == '__main__':
    win = TreeViewFilterWindow()
    Gtk.main()
