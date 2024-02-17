import datetime
import sys
from importlib.resources import Resource

sys.path.append("C:\\Users\\Admin\\PycharmProjects")
from autointellimini import db
from sqlalchemy.dialects.postgresql import JSON


class CategoryModel(db.Model):
    __tablename__ = 'ai_mini_category'
    categoryid = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(), nullable=False)

    def __init__(self, categoryname):
        self.categoryname = categoryname

    def __repr__(self):
        return f"<User {self.categoryname}>"


class SubCategoryModel(db.Model):
    __tablename__ = 'ai_mini_subcategory'
    scid = db.Column(db.Integer, primary_key=True)
    categoryid = db.Column(db.Integer, db.ForeignKey('ai_mini_category.categoryid'))
    categoryname = db.relationship("CategoryModel", backref=db.backref("Subcategorymodel", uselist=False))
    scname = db.Column(db.String(), nullable=False)

    def __init__(self, categoryid, scname):
        self.categoryid = categoryid
        self.scname = scname

    def __repr__(self):
        return f"<User {self.scname}>"


class FormModel(db.Model):
    __tablename__ = 'ai_mini_forms'
    formid = db.Column(db.Integer, primary_key=True)
    scid = db.Column(db.Integer, db.ForeignKey('ai_mini_subcategory.scid'))
    scname = db.relationship("SubCategoryModel", backref=db.backref("ai_mini_subcategorymodel", uselist=False))
    formdata = db.Column(JSON, nullable=True)
    processname = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(), nullable=False)

    def __init__(self, scid, formdata, url, processname):
        self.scid = scid
        self.formdata = formdata
        self.url = url
        self.processname = processname

    def __repr__(self):
        return f"<User {self.url}>"



