import json

class UserManager:
    def __init__(self):
        self.users = []
        self.db_connection = None
        self.email_config = {"host": "smtp.mail.com", "port": 587}

    def connect_db(self, host, port, db):
        self.db_connection = {"host": host, "port": port, "db": db}
        print("Connected to " + host)

    def add_user(self, name, email, age, role):
        if name == "" or email == "":
            print("Error: empty fields")
            return False
        if "@" not in email:
            print("Error: invalid email")
            return False
        if age < 0 or age > 150:
            print("Error: invalid age")
            return False
        user = {"name": name, "email": email, "age": age, "role": role}
        self.users.append(user)
        # send welcome email
        import smtplib
        try:
            server = smtplib.SMTP(self.email_config["host"], self.email_config["port"])
            server.sendmail("admin@app.com", email, "Welcome " + name)
            server.quit()
        except:
            print("Failed to send email")
        # log to file
        f = open("users.log", "a")
        f.write("Added user: " + name + "\n")
        f.close()
        return True

    def delete_user(self, email):
        for i in range(len(self.users)):
            if self.users[i]["email"] == email:
                del self.users[i]
                f = open("users.log", "a")
                f.write("Deleted user: " + email + "\n")
                f.close()
                return True
        return False

    def find_user(self, email):
        for u in self.users:
            if u["email"] == email:
                return u
        return None

    def export_users(self, filename):
        f = open(filename, "w")
        f.write(json.dumps(self.users))
        f.close()

    def get_users_by_role(self, role):
        result = []
        for u in self.users:
            if u["role"] == role:
                result.append(u)
        return result

    def send_email_to_all(self, message):
        import smtplib
        for u in self.users:
            try:
                server = smtplib.SMTP(self.email_config["host"], self.email_config["port"])
                server.sendmail("admin@app.com", u["email"], message)
                server.quit()
            except:
                print("Failed to send to " + u["email"])
