from django.db import models

class Menu(models.Model):
    menu_id = models.AutoField(db_column='Menu_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('account.User', models.CASCADE, db_column='User_ID')  # Field name made lowercase.
    meal_day = models.DateField(db_column='Meal_Day', max_length=10)  # Field name made lowercase.
    mealtime = models.CharField(db_column='MealTime', max_length=1)  # Field name made lowercase.

    class Meta:
        
        db_table = 'menu'

class Menucook(models.Model):
    menucook_id = models.AutoField(db_column='menucook_ID', primary_key=True)  # Field name made lowercase.
    menu = models.ForeignKey('healthmanagement.Menu', models.CASCADE, db_column='Menu_ID')  # Field name made lowercase.
    cook = models.ForeignKey('administrator.Cook', models.CASCADE, db_column='Cook_ID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'menucook'