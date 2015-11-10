package se.uu.csproject.monadclient;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;

public class AboutUsActivity extends MenuedActivity {

    private Toolbar toolbar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_about_us);

        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
    }

//    @Override
//    public boolean onCreateOptionsMenu(Menu menu) {
//
//        if(ClientAuthentication.getPassword().equals("0")){
//            // Inflate the menu; this adds items to the action bar if it is present.
//            getMenuInflater().inflate(R.menu.menu_main_google, menu);
//            return true;
//        }
//        else {
//            getMenuInflater().inflate(R.menu.menu_main, menu);
//            return true;
//        }
//    }
//
//    @Override
//    public boolean onOptionsItemSelected(MenuItem item) {
//        // Handle action bar item clicks here. The action bar will
//        // automatically handle clicks on the Home/Up button, so long
//        // as you specify a parent activity in AndroidManifest.xml.
//        int id = item.getItemId();
//
//        if (id == R.id.action_search) {
//            startActivity(new Intent(this, MainActivity.class));
//        }
//
//        if (id == R.id.action_notifications) {
//            startActivity(new Intent(this, NotificationsActivity.class));
//        }
//
//        if (id == R.id.action_mytrips) {
//            startActivity(new Intent(this, TripsActivity.class));
//        }
//
//        if (id == R.id.action_profile) {
//            startActivity(new Intent(this, ProfileActivity.class));
//        }
//
//        //noinspection SimplifiableIfStatement
//        if (id == R.id.action_settings) {
//            startActivity(new Intent(this, SettingsActivity.class));
//        }
//
//        if (id == R.id.action_aboutus) {
//            //TODO (low priority): Create a toaster with text about the MoNAD project and team
//            return true;
//        }
//
//        if (id == R.id.action_signout) {
//            startActivity(new Intent(this, LoginActivity.class));
//        }
//
//        return super.onOptionsItemSelected(item);
//    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if(id == R.id.action_aboutus){
            return true;
        }
        else {
            return super.onOptionsItemSelected(item);
        }
    }
}
