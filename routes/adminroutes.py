from importlib.resources import Resource
from urllib.parse import urlparse
import datetime
import json
from functools import wraps
import jwt
import requests
# import shortuuid
from flask import current_app as app
from flask import request, abort, jsonify

# autoincrement/routes/adminroutes.py
# from flask_sqlalchemy import Pagination
# from passlib.hash import sha256_crypt
# from requests import ConnectTimeout
# from sqlalchemy import func
from models.models import db, CategoryModel, SubCategoryModel, FormModel


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'Session-Key' not in request.headers:
            abort(401)
        user = None
        token = request.headers['Session-Key'].replace('"', '')
        try:
            user = jwt.decode(token, "Test", leeway=30, algorithms=['HS256'])
        except Exception as e:
            print(str(e))
            abort(401)
        return f(user, *args, **kws)

    return decorated_function


# @app.route('/api/admin/createCategory', methods=['POST'])
# @authorize
# def create_category(*args):
#     return jsonify(status=True, message="Hello World"), 200


# category
# View all categories
@app.route("/api/View_Category", methods=["GET"])
def view_all_categories():
    if request.method == "GET":
        try:
            categories = CategoryModel.query.all()
            category_list = [{"id": category.categoryid, "category_name": category.categoryname} for category in
                             categories]
            return jsonify({"category": category_list})
        except Exception as e:
            app.logger.error(f"Error in view all category operation: {str(e)}")
            return jsonify({"message": "Internal Server Error", "error": str(e)}), 500


# Add a new category
@app.route("/api/Add_Category", methods=["POST"])
def add_category():
    if request.method == "POST":
        try:
            data = request.get_json()
            new_category_name = data.get("category_name")

            if not new_category_name:
                return jsonify({"message": "Category name is required"}), 400

            # Check if the category with the same name already exists
            existing_category = CategoryModel.query.filter_by(categoryname=new_category_name).first()

            if existing_category:
                return jsonify({"message": "Category with this name already exists"}), 400

            new_category = CategoryModel(categoryname=new_category_name)
            db.session.add(new_category)
            db.session.commit()

            return jsonify({"message": "Category added successfully"})
        except Exception as e:
            app.logger.error(f"Error in adding a new category: {str(e)}")
            return jsonify({"message": "Internal Server Error", "error": str(e)}), 500


# Update a category by ID
@app.route("/api/Update_Category/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    if request.method == "PUT":
        try:
            data = request.get_json()
            updated_category_name = data.get("category_name")

            if not updated_category_name:
                return jsonify({"message": "Category name is required"}), 400

            # Check if the category with the given ID exists
            existing_category = CategoryModel.query.get(category_id)

            if not existing_category:
                return jsonify({"message": "Category not found"}), 404

            # Check if the updated category name already exists
            if updated_category_name != existing_category.categoryname:
                duplicate_category = CategoryModel.query.filter_by(categoryname=updated_category_name).first()
                if duplicate_category:
                    return jsonify({"message": "Category with this name already exists"}), 400

            existing_category.categoryname = updated_category_name
            db.session.commit()

            return jsonify({"message": "Category updated successfully"})
        except Exception as e:
            app.logger.error(f"Error in updating the category: {str(e)}")
            return jsonify({"message": "Internal Server Error", "error": str(e)}), 500


# Delete a category by ID
@app.route("/api/Delete_Category/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    try:
        category = CategoryModel.query.get(category_id)

        if not category:
            return jsonify({"message": "Category not found"}), 404

        db.session.delete(category)
        db.session.commit()

        return jsonify({"message": "Category deleted successfully"})
    except Exception as e:
        app.logger.error(f"Error in delete category operation: {str(e)}")
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500


# subcategory
# API to view all subcategories for a category
@app.route("/api/view_subcategories/<int:category_id>", methods=["GET"])
def view_subcategories(category_id):
    try:
        category = CategoryModel.query.get(category_id)

        if not category:
            return jsonify({"message": "Category not found"}), 404

        subcategories = SubCategoryModel.query.filter_by(categoryid=category_id).all()

        subcategory_list = [{"id": subcategory.scid, "subcategoryname": subcategory.scname} for subcategory in
                            subcategories]

        return jsonify({"subcategories": subcategory_list})
    except Exception as e:
        app.logger.error(f"Error in view subcategories operation: {str(e)}")
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500


@app.route("/api/Add_Subcategory/<int:category_id>", methods=["POST"])
def add_Subcategory(category_id):
    try:
        category = CategoryModel.query.get(category_id)

        if not category:
            return jsonify({"message": "Category not found"}), 404

        data = request.get_json()
        new_subcategory_name = data.get("subcategory_name")

        if not new_subcategory_name:
            return jsonify({"message": "Subcategory name is required"}), 400

        # Check if the subcategory with the same name already exists in the category
        existing_subcategory = SubCategoryModel.query.filter_by(categoryid=category_id,
                                                                scname=new_subcategory_name).first()
        if existing_subcategory:
            return jsonify({"message": "Subcategory with the same name already exists"}), 400

        new_subcategory = SubCategoryModel(categoryid=category_id, scname=new_subcategory_name)
        db.session.add(new_subcategory)
        db.session.commit()

        return jsonify({"message": "Subcategory added successfully"})
    except Exception as e:
        app.logger.error(f"Error in adding a new subcategory: {str(e)}")
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500


# Update a subcategory by ID
@app.route("/api/Update_Subcategory/<int:subcategory_id>", methods=["PUT"])
def update_subcategory(subcategory_id):
    try:
        data = request.get_json()
        updated_subcategory_name = data.get("subcategory_name")

        subcategory = SubCategoryModel.query.get(subcategory_id)

        if not subcategory:
            return jsonify({"message": "Subcategory not found"}), 404

        # Check if the updated subcategory name already exists
        existing_subcategory = SubCategoryModel.query.filter_by(categoryid=subcategory.categoryid,
                                                                scname=updated_subcategory_name).first()
        if existing_subcategory:
            return jsonify({"message": "Subcategory with the updated name already exists"}), 400

        subcategory.scname = updated_subcategory_name
        db.session.commit()

        return jsonify({"message": "Subcategory updated successfully"})
    except Exception as e:
        app.logger.error(f"Error in update subcategory operation: {str(e)}")
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500


# Delete a subcategory by ID
@app.route("/api/Delete_Subcategory/<int:subcategory_id>", methods=["DELETE"])
def delete_subcategory(subcategory_id):
    try:
        subcategory = SubCategoryModel.query.get(subcategory_id)

        if not subcategory:
            return jsonify({"message": "Subcategory not found"}), 404

        db.session.delete(subcategory)
        db.session.commit()

        return jsonify({"message": "Subcategory deleted successfully"})
    except Exception as e:
        app.logger.error(f"Error in delete subcategory operation: {str(e)}")
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500


# FormModel
@app.route('/api/Add/Form', methods=['POST'])
def create_form():
    try:
        data = request.json

        scid = data.get('scid')
        formdata = data.get('formdata')
        url = data.get('url')
        processname = data.get('processname')

        # Check if a form with the given scid already exists
        existing_form = FormModel.query.filter_by(scid=scid).first()

        if existing_form:
            return jsonify({"message": f"Form with scid {scid} already exists"}), 409

        new_form = FormModel(scid=scid, formdata=formdata, url=url, processname=processname)

        db.session.add(new_form)
        db.session.commit()

        return jsonify({"message": "Form created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/Get_Form/<int:scid>', methods=['GET'])
def get_form_data(scid):
    try:
        # Find the SubCategoryModel instance based on scid
        subcategory = SubCategoryModel.query.filter_by(scid=scid).first()

        if subcategory:
            # Find the associated FormModel instance based on scid
            form = FormModel.query.filter_by(scid=scid).first()

            if form:
                # Return form data as JSON
                return jsonify({
                    'sub_category_name': subcategory.scname,
                    'form_data': form.formdata,
                    'url': form.url,
                    'processname': form.processname
                })
            else:
                return jsonify({'error': 'Form data not found for the given subcategory ID'}), 404
        else:
            return jsonify({'error': 'Subcategory not found for the given ID'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/Update/Form/<int:form_id>', methods=['PUT'])
def update_form(form_id):
    form = FormModel.query.get(form_id)

    if not form:
        return jsonify({"error": "Form not found"}), 404

    data = request.json
    form.scid = data.get('scid', form.scid)
    form.formdata = data.get('formdata', form.formdata)
    form.url = data.get('url', form.url)
    form.processname = data.get('processname', form.processname)

    db.session.commit()

    return jsonify({"message": "Form updated successfully"})


@app.route('/api/Delete/Form/<int:form_id>', methods=['DELETE'])
def delete_form(form_id):
    form = FormModel.query.get(form_id)
    if not form:
        return jsonify({"error": "Form not found"}), 404

    db.session.delete(form)
    db.session.commit()

    return jsonify({"message": "Form deleted successfully"})
