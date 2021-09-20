from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import PitchForm,CommentForm, UpdateProfile
from ..models import User,Pitch,Comments
from flask_login import login_required,current_user
from .. import db,photos
import markdown2  



# Views

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data

    '''

    all_pitches=Pitch.query.order_by('id').all()
    print(all_pitches)
    title='Pitches App'
    return render_template('index.html',title=title)
@main.route('/pitch/newpitch', methods=['POST', 'GET'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        newPitch = form.pitch_info.data
        #update pitch instance
        new_pitch = Pitch(pitch_title=title,
                          pitch_category=category,
                          pitch_itself=newPitch,
                          user=current_user)
        #save pitch
        new_pitch.save_pitch()
        return redirect(url_for('.index'))
    title = 'Add New pitch'
    return render_template('pitches.html', title=title, pitchesform=form)
@main.route('/category/sports')
def sports():
    '''
    view function to display sports pitches
    '''
    pitches=Pitch.get_pitches('sports')
    sports_title ='sports Pitches'
    return render_template('pitches/sports.html',title=sports_title,sports_pitch=pitches)
@main.route('/category/business')
def business():
    '''
    view function to display business pitches
    '''
    pitches=Pitch.get_pitches('business')
    business_title='Business Pitches'
    return render_template('pitches/business.html',title=business_title, business_pitch=pitches)

@main.route('/category/politics')
def politics():
    '''
    view function to display business pitches
    '''
    pitches=Pitch.get_pitches('politics')
    politics_title = 'Politics Pitches'
    return render_template('pitches/politics.html',title=politics_title,politics_pitch=pitches)

@main.route('/comment/<int:id>', methods=['POST', 'GET'])
@login_required
def post_comment(id):
    pitche = Pitch.getPitchId(id)
    comments = Comments.get_comments(id)
    if request.args.get("like"):
        pitch = Pitch.query.filter_by(user_id=current_user.id)
        pitch.likes += 1
        print(pitch.likes)
        db.session.add(pitch.likes)
        db.session.commit()
        return str(pitch.likes)
    elif request.args.get("dislike"):
        pitche.dislikes += 1
        db.session.add()
        db.session.commit()
        return redirect(".comment")
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comments(comment_itself=comment,
                               user_id=current_user.id,
                               pitches_id=pitche.id)
        new_comment.save_comment()
        return redirect(url_for('main.post_comment', id=pitche.id))
    return render_template('comment.html',
                           commentform=form,
                           comments=comments,
                           pitch=pitche)
@main.route('/pitch/upvote/<int:id>&<int:vote>')
@login_required
def vote(id, vote):
    counter = 0
    pitchethrill = Pitch.getPitchId(id)
    # vote = .get_vote(id)
    counter += 1
    print(counter)
    new_vote = Pitch(likes=counter)
    new_vote.save_vote()
    return str(new_vote)


@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname = user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<uname>/update/pic',methods = ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname = uname))

    







