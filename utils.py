from flask import request, Response, redirect
import json

MASON = "application/vnd.mason+json"


class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href


class ModelBuilder(MasonBuilder):

    def add_controls_users_coll(self):
        self.add_control(
            ctrl_name="self",
            href="/api/users/",
        )
        self.add_control(
            ctrl_name="add",
            href="/api/users/",
            method="POST",
            encoding="json",
            title="Add user to the Journey Diary API",
            schema=user_schema()
        )

    def add_controls_user_item(self, userid):
        self.add_control(
            ctrl_name="self",
            href="/api/users/" + str(userid) + "/"
        )
        self.add_control(
            ctrl_name="edit",
         			href="/api/users/" + str(userid) + "/",
         			method="PUT",
      		    encoding="json",
      		    title="Modify one user to the Journey Diary API",
   	        schema=user_schema()
        )
        self.add_control(
            ctrl_name="delete",
         			href="/api/users/" + str(userid) + "/",
         			method="DELETE",
      		    title="Delete one user of the Journey Diary API"
        )
        self.add_control(
            ctrl_name="up",
            href="/api/users/",
      		    title="Collection of users"
        )
        self.add_control(
            ctrl_name="journeys-by",
            href="/api/users/" + str(userid) + "/journeys/",
      		    title="Collection of journeys associated to this user"
        )

    def add_controls_journeys_coll(self, userid):
        self.add_control(
            ctrl_name="self",
            href="/api/users/" + str(userid) + "/journeys/"
        )
        self.add_control(
            ctrl_name="add",
            href="/api/users/" + str(userid) + "/journeys/",
            method="POST",
            encoding="json",
            title="Add Journey to the Journey Diary API",
            schema=journey_schema()
        )
        self.add_control(
            ctrl_name="author",
            href="/api/users/" + str(userid) + "/",
      		    title="User related to this collection of Journeys"
        )

    def add_controls_journey_item(self, userid, journeyid):
        self.add_control(
            ctrl_name="self",
            href="/api/users/" + str(userid) +
            "/journeys/" + str(journeyid) + "/"
        )
        self.add_control(
            ctrl_name="edit",
         			href="/api/users/" + str(userid) +
            "/journeys/" + str(journeyid) + "/",
         			method="PUT",
      		    encoding="json",
      		    title="Modify one journey to the Journey Diary API",
   	        schema=journey_schema()
        )
        self.add_control(
            ctrl_name="delete",
         			href="/api/users/" + str(userid) +
            "/journeys/" + str(journeyid) + "/",
         			method="DELETE",
      		    title="Delete one journey of the Journey Diary API"
        )
        self.add_control(
            ctrl_name="up",
            href="/api/users/" + str(userid) + "/journeys/",
      		    title="Collection of journeys of this journey"
        )
        self.add_control(
            ctrl_name="days-by",
            href="/api/users/" + str(userid) +
            "/journeys/" + str(journeyid) + "/days/",
      		    title="Collection of days associated to this journey"
        )

    def add_controls_days_coll(self, userid, journeyid):
        self.add_control(
            ctrl_name="self",
            href="/api/users/" + str(userid) +
            "/journeys/" + str(journeyid) + "/days/"
        )
        self.add_control(
            ctrl_name="add",
            href="/api/users/" + str(userid) +
            "/journeys/" + str(journeyid) + "/days/",
            method="POST",
            encoding="json",
            title="Add Day to the Journey Diary API",
            schema=day_schema()
        )
        self.add_control(
            ctrl_name="journey-of",
            href="/api/users/" + str(userid) +
            "/journeys/" + str(journeyid) + "/",
      		    title="Journey related to this collection of Days"
        )

    def add_controls_day_item(self, userid, journeyid, dayid):
        self.add_control(
            ctrl_name="self",
            href="/api/users/" + str(userid) + "/journeys/" +
            str(journeyid) + "/days/" + str(dayid) + "/"
        )
        self.add_control(
            ctrl_name="edit",
         			href="/api/users/" + str(userid) + "/journeys/" +
            str(journeyid) + "/days/" + str(dayid) + "/",
         			method="PUT",
      		    encoding="json",
      		    title="Modify one day to the Journey Diary API",
   	        schema=day_schema()
        )
        self.add_control(
            ctrl_name="delete",
         			href="/api/users/" + str(userid) + "/journeys/" +
            str(journeyid) + "/days/" + str(dayid) + "/",
         			method="DELETE",
      		    title="Delete one day of the Journey Diary API"
        )
        self.add_control(
            ctrl_name="up",
            href="/api/users/" + str(userid) +
            "/journeys/" + str(journeyid) + "/days/",
      		    title="Collection of days of this day"
        )
        self.add_control(
            ctrl_name="images-by",
            href="/api/users/" + str(userid) + "/journeys/" +
            str(journeyid) + "/days/" + str(dayid) + "/images/",
      		    title="Collection of images associated to this day"
        )

    def add_controls_images_coll(self, userid, journeyid, dayid):
        self.add_control(
            ctrl_name="self",
            href="/api/users/" + str(userid) + "/journeys/" +
            str(journeyid) + "/days/" + str(dayid) + "/images/"
        )
        self.add_control(
            ctrl_name="add",
            href="/api/users/" + str(userid) + "/journeys/" +
            str(journeyid) + "/days/" + str(dayid) + "/images/",
            method="POST",
            encoding="json",
            title="Add Image to the Journey Diary API",
            schema=image_schema()
        )
        self.add_control(
            ctrl_name="day-of",
            href="/api/users/" + str(userid) + "/journeys/" +
            str(journeyid) + "/days/" + str(dayid) + "/",
      		    title="Day related to this collection of Images"
        )

    def add_controls_image_item(self, userid, journeyid, dayid, imageid):
        self.add_control(
            ctrl_name="self",
            href="/api/users/" + str(userid) + "/journeys/" + str(journeyid) +
            "/days/" + str(dayid) + "/images/" + imageid + "/"
        )
        self.add_control(
            ctrl_name="edit",
         			href="/api/users/" + str(userid) + "/journeys/" + str(journeyid) +
            "/days/" + str(dayid) + "/images/" + imageid + "/",
         			method="PUT",
      		    encoding="json",
      		    title="Modify one image to the Journey Diary API",
   	        schema=image_schema()
        )
        self.add_control(
            ctrl_name="delete",
         			href="/api/users/" + str(userid) + "/journeys/" + str(journeyid) +
            "/days/" + str(dayid) + "/images/" + imageid + "/",
         			method="DELETE",
      		    title="Delete one image of the Journey Diary API"
        )
        self.add_control(
            ctrl_name="up",
            href="/api/users/" + str(userid) + "/journeys/" +
            str(journeyid) + "/days/" + str(dayid) + "/images/",
      		    title="Collection of images of this image"
        )


def create_error_response(status_code, title, message=None):
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    return Response(json.dumps(body), status_code, mimetype=MASON)


def user_schema():
    schema = {
        "type": "object",
        "required": ["username", "password", "email"]
    }
    props = schema["properties"] = {}
    props["username"] = {
        "description": "Username of the user",
        "type": "string"
    }
    props["password"] = {
        "description": "Password of the user",
        "type": "string"
    }
    props["email"] = {
        "description": "Email of the user",
        "type": "string"
    }
    return schema


def journey_schema():
    schema = {
        "type": "object",
        "required": ["title"]
    }
    props = schema["properties"] = {}
    props["title"] = {
        "description": "Title of the journey",
        "type": "string"
    }
    return schema


def day_schema():
    schema = {
        "type": "object",
        "required": ["date", "description"]
    }
    props = schema["properties"] = {}
    props["date"] = {
        "description": "Date of the day",
        "type": "string"
    }
    props["description"] = {
        "description": "Description of the day",
        "type": "string"
    }
    return schema


def image_schema():
    schema = {
        "type": "object",
        "required": ["extension"]
    }
    props = schema["properties"] = {}
    props["extension"] = {
        "description": "Extension of the image",
        "type": "string"
    }
    return schema
