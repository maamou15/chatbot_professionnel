from models.database import db

class JobRecommandation(db.Model):
    __tablename__ = 'job_recommandations'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    localisation = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<JobRecommandation {self.titre}>'
