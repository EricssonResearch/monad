package se.uu.csproject.monadclient;

import android.content.Intent;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;

import android.view.View;
import android.widget.ImageButton;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.List;

import se.uu.csproject.monadclient.recyclerviews.Trip;
import se.uu.csproject.monadclient.recyclerviews.TripRecyclerViewAdapter;


public class TripsActivity extends AppCompatActivity {
    Toolbar toolbar;
    ImageButton button;

    //TODO Ilyass: (high priority) Make specific trips selectable
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trips);
        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        List<Trip> trips = new ArrayList<>();
        RecyclerView recyclerView = (RecyclerView) findViewById(R.id.recycler_view_active);
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(getApplicationContext());
        recyclerView.setLayoutManager(linearLayoutManager);
        generateTrips(trips);
        TripRecyclerViewAdapter adapter = new TripRecyclerViewAdapter(trips);
        recyclerView.setAdapter(adapter);
    }

    public void cancelTrip(View view) {
        startActivity(new Intent(this, TripCancelPopup.class));
    }

    /*public void viewTripDetails(View view) {
        startActivity(new Intent(this, RouteActivity.class));
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
            //TODO (low priority): Create a toaster with text about the MoNAD project and team
            startActivity(new Intent(this, AboutUsActivity.class));
        }

        if (id == R.id.action_signout) {
            startActivity(new Intent(this, LoginActivity.class));
        }

        return super.onOptionsItemSelected(item);
    }

    //TEMPORARY FUNCTION TODO: Remove this function once the database connection is set
    private void generateTrips(List<Trip> trips){
        Calendar calendar = new GregorianCalendar(2015, 9, 26, 13, 40, 0);
        Date startdate1 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 9, 26, 13, 45, 0);
        Date enddate1 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 9, 26, 19, 55, 0);
        Date startdate2 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 9, 26, 20, 0, 0);
        Date enddate2 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 9, 27, 11, 50, 0);
        Date startdate3 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 9, 27, 12, 5, 0);
        Date enddate3 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 9, 22, 11, 30, 0);
        Date startdate4 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 9, 22, 12, 0, 0);
        Date enddate4 = calendar.getTime();
        trips.add(new Trip(1, "Polacksbacken",startdate1,"Flogsta", enddate1, 10, 0));
        trips.add(new Trip(2, "Gamla Uppsala",startdate2,"Gottsunda", enddate2, 15, 0));
        trips.add(new Trip(3, "Granby",startdate3,"Tunna Backar", enddate3, 15, 0));
        trips.add(new Trip(4, "Kungsgatan", startdate4, "Observatoriet", enddate4, 30, 0));
    }
}