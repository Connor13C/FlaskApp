from flask_restful import Resource
from flask import render_template, Response


class FrontPage(Resource):
    @staticmethod
    def get():
        return Response(render_template('resume.html'), mimetype='text/html')
