from django.db import models

class Menu(models.Model):
    menu_id = models.AutoField(db_column='Menu_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('account.User', models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    meal_day = models.DateTimeField(db_column='Meal_Day', max_length=10)  # Field name made lowercase.
    mealtime = models.CharField(db_column='MealTime', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'menu'