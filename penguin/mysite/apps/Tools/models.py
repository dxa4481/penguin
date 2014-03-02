from django.db import models

from ..Users.models import User

class Tool(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=30)
        #owner = models.ForeignKey('User')
        is_available = models.BooleanField(default=True)
        description = models.CharField(max_length=250)
        tool_type = models.CharField(max_length=30)

        """ Constructor to add a new tool
        :param n: name of tool
        :param d: description of tool
        :param t: type of tool
        :return The tool that was just added
        """
        def add_new_tool(self, n, d, tt):
                t = Tool(name=n, description=d, tool_type=tt)
                t.save()
                return t

        """ Deletes the given tool
        """
        def delete_tool(self):
                self.delete()

        """Sets a tool as unavailable
        """
        def set_tool_unavailable(self):
                self.is_available = False
                self.save()

        """ Sets a tool as available
        """
        def set_tool_available(self):
                self.is_available = True
                self.save()

        """Checks if tool is available
        :return true if available, false otherwise
        """
        def is_tool_available(self):
                if (self.is_available==True):
                        return True
                else:
                        return False

        """ Get tool's owner's id
        :return owner's id
        """
        def get_tool_owner(self):
                return OwnTool.filter(tool=self.id).owner

        """ Return tool's ID
        """
        def get_tool_id(self):
                return self.id

        """ Returns tool based on ID
        """
        def get_tool(toolID):
                return Tool.objects.filter(pk=toolID)


class OwnTool(models.Model):
        id = models.AutoField(primary_key=True)
        owner = models.ForeignKey(User)
        tool = models.ForeignKey(Tool)

        """Create a new tool ownership
        :param o: owner object
        :param t: tool object
        """
        def add_new_tool_ownership(o, t):
                own = OwnTool(owner=User.get_user(o),
                tool=Tool.get_tool(t))
                own.save()

        """ Remove a tool ownership
        """
        def remove_tool_ownership(self):
                self.delete()

        """ Return a tool ownership by id
        """
        #Not implemented. What should this return?      
        def get_tool_ownership(id):
                return null

        """Get a tool ownership's id
        :return id of tool ownership
        """
        def get_tool_ownership_id(self):
                return self.id

