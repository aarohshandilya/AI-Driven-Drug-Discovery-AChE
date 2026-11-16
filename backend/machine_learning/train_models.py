"""Train RF/SVM with scaffold-group holdout. Metrics reflect this run only."""
import argparse, json
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupShuffleSplit, GroupKFold, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix
from sklearn.dummy import DummyClassifier
import joblib

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',default='data/processed/ache_curated.csv');p.add_argument('--out',default='results');a=p.parse_args()
 d=pd.read_csv(a.input); X=d.filter(regex=r'^(fp_\d+|mw|logp|tpsa|hbd|hba|rotatable_bonds)$'); y=d.active.astype(int); groups=d.scaffold.fillna(d.smiles)
 train,test=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(X,y,groups));
 if y.iloc[train].nunique()<2 or y.iloc[test].nunique()<2: raise SystemExit('Scaffold split produced a single class; dataset needs further curation or another split strategy.')
 cv=GroupKFold(n_splits=min(5,groups.iloc[train].nunique()))
 candidates={'RandomForest':(RandomForestClassifier(class_weight='balanced',random_state=42,n_jobs=1),{'n_estimators':[100],'max_depth':[None,20],'min_samples_leaf':[1,3]}),'SVM':(make_pipeline(StandardScaler(),SVC(class_weight='balanced',random_state=42)),{'svc__C':[0.1,1,10],'svc__kernel':['rbf']})}
 reports={};Path(a.out).mkdir(parents=True,exist_ok=True)
 for name,(model,grid) in candidates.items():
  splits=list(cv.split(X.iloc[train],y.iloc[train],groups.iloc[train]))
  search=GridSearchCV(model,grid,scoring='average_precision',cv=splits,n_jobs=1,refit=True);search.fit(X.iloc[train],y.iloc[train]);m=search.best_estimator_;pred=m.predict(X.iloc[test]);scores=m.predict_proba(X.iloc[test])[:,1] if hasattr(m,'predict_proba') else m.decision_function(X.iloc[test])
  reports[name]={'best_params':search.best_params_,'accuracy':accuracy_score(y.iloc[test],pred),'precision':precision_score(y.iloc[test],pred,zero_division=0),'recall':recall_score(y.iloc[test],pred,zero_division=0),'f1':f1_score(y.iloc[test],pred,zero_division=0),'roc_auc':roc_auc_score(y.iloc[test],scores),'pr_auc':average_precision_score(y.iloc[test],scores),'confusion_matrix':confusion_matrix(y.iloc[test],pred).tolist(),'train_n':len(train),'test_n':len(test)}
  joblib.dump(m,Path(a.out)/f'{name.lower()}_model.joblib')
 (Path(a.out)/'metrics.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports,indent=2))
if __name__=='__main__':main()
