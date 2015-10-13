package se.uu.csproject.monadclient;

import android.content.Intent;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;

import android.view.View;
import android.widget.ImageButton;


public class TripsActivity extends AppCompatActivity {
    //ImageButton detailsButton1;
    //ImageButton cancelButton1;
    //ImageButton imgButton;
    Toolbar toolbar;
    ImageButton button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trips);
        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

    }

    public void cancelTrip(View view) {
        startActivity(new Intent(this, TripCancelPopup.class));
    }

    public void viewTripDetails(View view) {
        startActivity(new Intent(this, RouteActivity.class));
    }

    /*public void cancelTrip2(View view) {
        Intent intent = new Intent(this, TripCancelPopup.class);
        cancelButton1 = (ImageButton) findViewById(R.id.cancel2);
        startActivity(intent);
    }*/

    /*public void viewTripDetails1(View view) {
        Intent intent = new Intent(this, RouteActivity.class);
        detailsButton1 = (ImageButton) findViewById(R.id.button1);
        startActivity(intent);
    }*/

   /* public void viewTripDetails2(View view) {
        Intent intent = new Intent(this, RouteActivity.class);
        detailsButton1 = (ImageButton) findViewById(R.id.button2);
        startActivity(intent);
    }*/

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        if (id == android.R.id.home) {
            NavUtils.navigateUpFromSameTask(this);
        }

        if (id == R.id.action_search) {
            startActivity(new Intent(this, MainActivity.class));
        }

        if (id == R.id.action_notifications) {
            startActivity(new Intent(this, NotificationsActivity.class));
        }

        if (id == R.id.action_mytrips) {
            return true;
        }

        if (id == R.id.action_profile) {
            startActivity(new Intent(this, ProfileActivity.class));
        }

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            startActivity(new Intent(this, SettingsActivity.class));
        }

        if (id == R.id.action_aboutus) {
            //TODO: Create a toaster with text about the MoNAD project and team
            startActivity(new Intent(this, AboutUsActivity.class));
        }

        if (id == R.id.action_signout) {
            startActivity(new Intent(this, LoginActivity.class));
        }

        return super.onOptionsItemSelected(item);
    }
}