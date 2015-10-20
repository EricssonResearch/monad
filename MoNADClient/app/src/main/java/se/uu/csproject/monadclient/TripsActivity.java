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

    public void viewTripDetails(View view) {
        startActivity(new Intent(this, RouteActivity.class));
    }

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
        trips.add(new Trip(1, "Polacksbacken","12:36","Flogsta", "12:51", 15, 2));
        trips.add(new Trip(2, "Polacksbacken","20:36","Flogsta", "20:51", 15, 4));
        trips.add(new Trip(3, "Gamla Uppsala","19:17","Övre Slottsgatan", "19:35", 18, 3));
        trips.add(new Trip(4, "Polacksbacken","12:36","Flogsta", "12:51", 15, 0));
    }
}