import sqlite3

TABLE = 'users'

def create_database_user(email=None,password=None,name=None):
  Dictionary  = {'name':name, 'email':email,'password':password}
  return Dictionary 
  #return new dictionary that stores the user information

class Database:
  def __init__(self):
    self.conn = sqlite3.connect('userInfo.db')
    self.conn.row_factory = self._row_facatory
    self.cursor = self.conn.cursor()
    self._create_table()

  def _row_facatory(self,cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

  def _create_table(self):
    query = f"""CREATE TABLE IF NOT EXISTS {TABLE}(
      name text,
      email text,
      password text,
      wins intiger,
      losses intiger,
      id INTEGER PRIMARY KEY AUTOINCREMENT 
    )"""
    with self.conn:
      self.cursor.execute(query)

  def insert_new_user(self, user):
    '''
    type user: disctionary
    rtype: None
    '''
    data = (user['name'],user['email'],user['password'],0,0,None)
    with self.conn:
      query = f'''INSERT INTO {TABLE} VALUES(?,?,?,?,?,?)'''
      self.cursor.execute(query,data)
  
  def update_wins(self,user):
    """
    type user: dictionary
    rtype: None
    """

    with self.conn:
      query = f"UPDATE {TABLE} SET wins = wins + 1 WHERE name =:name AND email =:email "
      self.cursor.execute(query,{'name':user['name'],'email':user['email']})
  def update_loss(self, user):
    '''
    type user: Dict 
    rtype: None
    '''
    with self.conn:
      query ='UPDATE {TABLE} SET losses = losses + 1 WHERE name =:name'
      self.cursor.execute(query,{'name':user['name']})

  def validate_user(self, user):
    '''
    type user: Dict
    rtype bool
    '''
    with self.conn:
      query = f'SELECT * FROM {TABLE} where email =:email AND password =:password'
      self.cursor.execute(query,{'email':user['email'], 'password':user['password']})

    value = self.cursor.fetchone()
    return True if value else False

  def get_user_info(self, userInfo):
    '''
    type userInfo: Dict
    rtype: Dict
    '''
    with self.conn:
      query = f'SELECT * FROM {TABLE} WHERE name =:name OR email =:email'
      self.cursor.execute(query,{'name':userInfo['name'],'email':userInfo['email']})
    data = self.cursor.fetchone()
    return data

  def get_all_users(self):
    query = f'SELECT * FROM {TABLE}'
    with self.conn:
      self.cursor.execute(query)
      ls = self.cursor.fetchall()
      return ls

if __name__ == '__main__':
  c = Database()
  user = {
    'name':'josh',
    'email':'josh@gmail.com',
    'password' : 'password123'
  }
  c.insert_new_user(user)
  #print(c.get_user_info(user))
  #print(c.validate_user(user))
  print(c.get_all_users())
  # vals = ['wins','losses']
  # c.update_data(vals)
      