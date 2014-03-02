from django.db import models


class User(models.Model):
        id = models.AutoField(primary_key=True)
        username = models.CharField(max_length=30)
        password = models.CharField(max_length=30)
        area_code = models.CharField(max_length=5)
        email = models.CharField(max_length=30)
        phone_number = models.CharField(max_length=10)
        is_shed_coordinator = models.BooleanField(default=False)
        is_admin = models.BooleanField(default=False)
        is_community_shed = models.BooleanField(default=False)

        def __str__(self):
                return (str(self.id) + ':' + self.username)

        """ Constructor for a user entry
        :param u: username string
        :param p: password string
        :param ac: area code string
        :param e: email string (forced email field type)
        :param pn: phone number string
        """
        def create_new_user(u, p, ac, e, pn):
                newuser = User(username=u, password=p,
                area_code=ac, email=e,
                phone_number=pn)
                newuser.save()

        """ Constructor for a community shed entry
        :param ac: area code, used as username as well
        """
        def create_new_community_shed(self, ac):
                cs = User(username=ac, password="",
                area_code=ac, email="", phone_number="",
                is_community_shed=True)
                cs.save()

        """ Returns a user based on user's ID
        :param userID: user's ID
        :return User object
        """
        def get_user(userID):
                return User.objects.get(pk=userID)

        """ Get a user ID
        :return user's ID
        """
        def get_user_id(self):
                return self.id

        """ Promotes user object to admin status
        """
        def promote_user_to_admin(self):
                self.is_admin = True;
                self.save()
        """ Demotes user object from admin status
        """
        def demote_user_from_admin(self):
                self.is_admin = False
                self.save()

        """ Promotes user object to shed coordinator
        """
        def promote_user_to_shed_coordinator(self):
                self.is_shed_coordinator = True
                self.save()

        """ Demotes user object from shed coordinator
        """
        def demote_user_from_shed_coordinator(self):
                if(self.is_shed_coordinator):
                        self.is_shed_coordinator = False;

        """ Returns an array(?) of all user's tools
        """
        def get_all_user_tools(self):
                ot = OwnTool.objects.filter(owner=self)
                tools = ot.tool_set
                return tools

        """ Deletes a user
        """
        def delete_user(self):
                self.tool_set.all().delete()
                self.delete()

        """Add a new tool to tools, then relate it to this user
        :param n: name of tool
        :param d: description of tool
        :param t: type of tool
        """
        def add_new_tool(self, n, d, t):
                t = Tool.add_new_tool(n, d, t)
                OwnTool.add_new_tool_ownership(self, t)

