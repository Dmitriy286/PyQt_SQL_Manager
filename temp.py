
        pb.clicked.connect(self.addNewUser)

        self.list_view_person = QtWidgets.QListView()
        self.list_view_person.clicked.connect(self.getUserInfo)

        self.loadUsers()

    def loadUsers(self):
        result = []
        for user in getAllUsers():
            result.append(f"{user.get('name')} {user.get('surname')}")

        sim = QtCore.QStringListModel(result)
        self.list_view_person.setModel(sim)


    def addNewUser(self):
        user = addUser()

        model = self.list_view_person.model()

        new_row = model.rowCount()
        model.insertRow(new_row)
        model.setData(model.index(new_row, 0), f"{user.get('name')} {user.get('surname')}")


    def getUserInfo(self):
        insert_row = self.list_view_person.selectionModel().selectedRows()[0]
        model = self.list_view_person.model()
        name, surname = tuple(model.data(insert_row).split(" "))
        users = getAllUsers()
        for user in users:
            if user.get('name') == name and user.get('surname') == surname:
                self.plain_text_edit_log.\
                    appendPlainText(f"Пользователь: {user.get('name')} {user.get('surname')}\n"
                                    f"Логин:              {user.get('login')}\n"
                                    f"Пароль:            {user.get('password')}\n"
                                    f"E-Mail:               {user.get('email')}\n"
                                    f"Телефон:         {user.get('phone')}\n"
                                    f"Дата рег.:       {user.get('register_time').isoformat()}\n")




