from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Schedule(db.Model):
  event_id = db.Column(db.Integer, primary_key=True)
  event_name = db.Column(db.String(200), nullable=False)
  event_start = db.Column(db.String(200), nullable=False)
  event_end = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)
  def __repr__(self):
    return '<Event ID %r>' % self.event_id

@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    e_name = request.form['name']
    e_start = request.form['start']
    e_end = request.form['end']
    n_event = Schedule(event_name=e_name, event_start=e_start, event_end=e_end)
    try:
       db.session.add(n_event)
       db.session.commit()
       return redirect('/')
    except:
      return 'there was an issue'
  else:
    events = Schedule.query.order_by(Schedule.date_created).all()
    return render_template('index.html', events=events)

@app.route('/delete/<int:id>')
def delete(id):
  event_to_delete = Schedule.query.get_or_404(id)
  try:
    db.session.delete(event_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return 'issue in deletion of event'

# @app.route('/update/<int:id>', methods=['GET','POST'])
# def update(id):
#   event = Schedule.query.get_or_404(id)
#   if request.method == 'POST':
#     e_name.name = request.form['name']
#     e_start.start = request.form['start']
#     e_end.end = request.form['end']
#     try:
#       db.session.commit()
#       return redirect('/')
#     except:
#       return 'an issue has happened'  
#   else:
#     return render_template('update.html', event=event)

if __name__ == "__main__":
  app.run(debug=True)