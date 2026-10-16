"""Train/evaluate an experimental loss-pathway text classifier from a reviewed CSV.

CSV columns: text,label. Labels must be reviewed by a qualified scheme expert.
The model is a triage/research aid only and must never decide eligibility or payment.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',required=True,help='Reviewed CSV with text,label columns')
    parser.add_argument('--out',default='ml/evaluation_report.json',help='JSON metrics report path')
    parser.add_argument('--model-out',default='ml/artifacts/loss_pathway_model.joblib',help='Serialized experimental pipeline path')
    parser.add_argument('--test-size',type=float,default=0.25)
    args=parser.parse_args()
    if not 0.1 <= args.test_size <= 0.4:
        raise SystemExit('--test-size must be between 0.1 and 0.4')
    df=pd.read_csv(args.data)   
    if not {'text','label'}.issubset(df.columns):
        raise SystemExit('CSV must contain text,label columns')
    df=df.dropna(subset=['text','label']).copy()
    df['text']=df['text'].astype(str).str.strip()
    df['label']=df['label'].astype(str).str.strip()
    df=df[(df.text!='') & (df.label!='')]
    if len(df)<30:
        raise SystemExit('At least 30 reviewed rows are required for this demo; more and balanced data are strongly recommended.')
    if df.label.nunique()<2:
        raise SystemExit('At least two label classes are required')
    counts=df.label.value_counts()
    if counts.min()<2:
        raise SystemExit('Each label must have at least two rows for stratified splitting')
    X_train,X_test,y_train,y_test=train_test_split(df.text,df.label,test_size=args.test_size,random_state=42,stratify=df.label)
    model=Pipeline([('tfidf',TfidfVectorizer(ngram_range=(1,2),min_df=1,max_features=20000,strip_accents='unicode')),('classifier',LogisticRegression(max_iter=1500,class_weight='balanced'))])
    model.fit(X_train,y_train)
    pred=model.predict(X_test)
    labels=sorted(df.label.unique().tolist())
    report={
      'model':'TF-IDF + LogisticRegression baseline', 'created_at_utc':datetime.now(timezone.utc).isoformat(),
      'rows':int(len(df)), 'train_rows':int(len(X_train)), 'test_rows':int(len(X_test)),
      'accuracy':float(accuracy_score(y_test,pred)), 'macro_f1':float(f1_score(y_test,pred,average='macro')),
      'labels':labels, 'class_counts':{str(k):int(v) for k,v in counts.items()},
      'classification_report':classification_report(y_test,pred,labels=labels,output_dict=True,zero_division=0),
      'confusion_matrix':confusion_matrix(y_test,pred,labels=labels).tolist(),
      'test_size':args.test_size, 'random_state':42,
      'disclaimer':'Results only measure this supplied dataset. Requires representative, expert-reviewed data and external validation. Never use for eligibility or compensation decisions.'
    }
    model_path=Path(args.model_out); model_path.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump(model,model_path)
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['model','rows','train_rows','test_rows','accuracy','macro_f1','labels','disclaimer']} ,indent=2))
    print('Metrics report:',out)
    print('Experimental model artifact:',model_path)

if __name__=='__main__': main()
