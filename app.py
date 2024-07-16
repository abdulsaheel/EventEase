from flask import Flask, session, redirect, url_for, render_template, request, jsonify, send_file

app = Flask(__name__)

app.secret_key = b'scretkey123'

