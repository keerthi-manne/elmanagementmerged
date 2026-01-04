from your_app import create_app, mysql

app = create_app()

def make_score_nullable():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🔧 Updating Evaluation Schema...")
        
        try:
            # Check current columns? Just force Modify
            # Assuming Score is FLOAT or DECIMAL(5,2) or INT
            # Safest is FLOAT or DECIMAL
            cur.execute("ALTER TABLE Evaluation MODIFY COLUMN Score FLOAT NULL")
            mysql.connection.commit()
            print("✅ Evaluation.Score is now NULLABLE.")
        except Exception as e:
            print(f"⚠️ Error updating schema (might already be nullable or type mismatch): {e}")

if __name__ == "__main__":
    make_score_nullable()
