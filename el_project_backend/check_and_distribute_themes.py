from your_app import create_app, mysql

app = create_app()

def distribute_themes():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🔍 Checking Project Theme Distribution...")
        
        # 1. Get all themes
        cur.execute("SELECT ThemeID, ThemeName FROM Theme")
        themes = cur.fetchall()
        theme_map = {t[1]: t[0] for t in themes}
        print(f"   Available Themes: {list(theme_map.keys())}")
        
        # 2. Get current distribution
        cur.execute("""
            SELECT t.ThemeName, COUNT(p.ProjectID) 
            FROM Project p 
            JOIN Theme t ON p.ThemeID = t.ThemeID 
            GROUP BY t.ThemeName
        """)
        dist = cur.fetchall()
        print("\n📊 Current Distribution:")
        for tname, count in dist:
            print(f"   - {tname}: {count}")
            
        # 3. Intelligent Redistribution based on Keywords
        print("\n🔧 Redistributing based on Title Keywords...")
        
        keywords = {
            'Blockchain': ['Blockchain', 'Crypto', 'Voting', 'Decentralized'],
            'IoT & Embedded': ['IoT', 'Smart', 'Automation', 'Traffic'],
            'Web Security': ['Security', 'Chat', 'Encryption'],
            'Cloud Computing': ['Cloud', 'SaaS', 'Serverless'],
            'Web Development': ['Web', 'Portal', 'E-Commerce'],
            'Machine Learning': ['AI', 'Prediction', 'Learning', 'Neural', 'Stock']
            # Fallback others to ML or Web Dev
        }
        
        updated_count = 0
        cur.execute("SELECT ProjectID, Title FROM Project")
        projects = cur.fetchall()
        
        for pid, title in projects:
            best_theme_id = None
            
            # Simple keyword match
            for theme_name, keys in keywords.items():
                if any(k.lower() in title.lower() for k in keys):
                    if theme_name in theme_map:
                        best_theme_id = theme_map[theme_name]
                        break
            
            # If no keyword match, maybe randomize or keep?
            # Let's leave it unless it was "Invalid" (which we fixed already)
            # But let's enforce keyword match if found.
            
            if best_theme_id:
                cur.execute("UPDATE Project SET ThemeID = %s WHERE ProjectID = %s", (best_theme_id, pid))
                updated_count += 1
                
        mysql.connection.commit()
        print(f"✅ Refined themes for {updated_count} projects based on their titles.")
        
        # 4. Final Verification
        cur.execute("""
            SELECT t.ThemeName, COUNT(p.ProjectID) 
            FROM Project p 
            JOIN Theme t ON p.ThemeID = t.ThemeID 
            GROUP BY t.ThemeName
        """)
        new_dist = cur.fetchall()
        print("\n📊 New Distribution:")
        for tname, count in new_dist:
            print(f"   - {tname}: {count}")

if __name__ == "__main__":
    distribute_themes()
