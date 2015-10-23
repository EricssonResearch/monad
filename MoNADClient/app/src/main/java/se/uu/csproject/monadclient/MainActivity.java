package se.uu.csproject.monadclient;

import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import se.uu.csproject.monadclient.recyclerviews.SearchRecyclerViewAdapter;
import se.uu.csproject.monadclient.recyclerviews.Trip;

public class MainActivity extends AppCompatActivity implements
        GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener, LocationListener {

    private Toolbar toolbar;
    private EditText destination;
    private GoogleApiClient mGoogleApiClient;
    private LocationRequest mLocationRequest;
    private double currentLatitude;
    private double currentLongitude;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        destination = (EditText) findViewById(R.id.main_search_destination);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        List<Trip> searchResults = new ArrayList<>();
        RecyclerView recyclerView = (RecyclerView) findViewById(R.id.recycler_view_main);
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(getApplicationContext());
        recyclerView.setLayoutManager(linearLayoutManager);
        generateSearchResults(searchResults);
        SearchRecyclerViewAdapter adapter = new SearchRecyclerViewAdapter(searchResults);
        recyclerView.setAdapter(adapter);
        buildGoogleApiClient();
        initializeLocationRequest();
        mGoogleApiClient.connect();
        if (mGoogleApiClient.isConnected()){
            Log.d("oops", "test3 passed");
        }
    }

    public void openMainSearch (View view) {
        // Make a quick search based on the current time and the user's current location
        String startPositionLatitude, startPositionLongitude, edPosition, userId, startTime, endTime;
        String requestTime, priority;
        Date now = new Date();
        SimpleDateFormat df = new SimpleDateFormat("yyyy EEE dd MMM HH:mm");

        // Provide some default values since this is a quick search
        startPositionLatitude = String.valueOf(currentLatitude);
        startPositionLongitude = String.valueOf(currentLongitude);
        edPosition = destination.getText().toString();
        userId = ClientAuthentication.getClientId();
        startTime = df.format(now);
        endTime = "null";
        requestTime = df.format(now);
        priority = "distance";

        Log.d("oops", "latitude: " + startPositionLatitude);
        Log.d("oops", "longitude: " + startPositionLongitude);
        new SendQuickTravelRequest().execute(userId, startTime, endTime, requestTime, startPositionLatitude,
                startPositionLongitude, edPosition, priority);

        Intent myIntent = new Intent(MainActivity.this, SearchActivity.class);
        MainActivity.this.startActivity(myIntent);
    }

    private void handleNewLocation(Location location) {
        currentLatitude = location.getLatitude();
        currentLongitude = location.getLongitude();
        Log.d("oops", "latitude1: " + currentLatitude);
        Log.d("oops", "longitude1: " + currentLongitude);
    }

    protected synchronized void buildGoogleApiClient() {
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(LocationServices.API)
                .build();

        Log.d("oops", "test1 passed");
    }

    protected void initializeLocationRequest() {
        mLocationRequest = LocationRequest.create()
                .setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY)
                .setInterval(10 * 1000)        // 30 seconds, in milliseconds
                .setFastestInterval(1 * 1000); // 1 second, in milliseconds

        Log.d("oops", "test2 passed");
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    public boolean onTouchEvent(MotionEvent event) {
        InputMethodManager imm = (InputMethodManager)getSystemService(Context.
                INPUT_METHOD_SERVICE);
        imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), 0);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        if(id == android.R.id.home){
            NavUtils.navigateUpFromSameTask(this);
        }

        if (id == R.id.action_search) {
            return true;
        }

        if (id == R.id.action_notifications) {
            startActivity(new Intent(this, NotificationsActivity.class));
        }

        if (id == R.id.action_mytrips) {
            startActivity(new Intent(this, TripsActivity.class));
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

    public void openTripDetail (View v) {
        //opens Route activity layout
        startActivity(new Intent(this, RouteActivity.class));
    }

    //TEMPORARY FUNCTION TODO: Remove this function once the database connection is set
    private void generateSearchResults(List<Trip> trips){
        trips.add(new Trip(1, "Polacksbacken","12:36","Flogsta", "12:51", 15, 2));
        trips.add(new Trip(2, "Polacksbacken","20:36","Flogsta", "20:51", 15, 4));
        trips.add(new Trip(3, "Gamla Uppsala","19:17","Övre Slottsgatan", "19:35", 18, 3));
        trips.add(new Trip(4, "Polacksbacken", "12:36", "Flogsta", "12:51", 15, 0));
    }

    @Override
    protected void onResume() {
        super.onResume();
        /*if (!mGoogleApiClient.isConnected()){
            mGoogleApiClient.connect();
        }*/
    }

    @Override
    protected void onPause() {
        super.onPause();
        /*if (mGoogleApiClient.isConnected()) {
            LocationServices.FusedLocationApi.removeLocationUpdates(mGoogleApiClient, this);
            mGoogleApiClient.disconnect();
        }*/
    }

    @Override
    public void onConnected(Bundle bundle) {
        Location location = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);

        if (location == null) {
            Log.d("oops", "Did not work, lets try smth!");
            LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient, mLocationRequest, this);
            Log.d("oops", "Something was tried!");
        }
        else {
            Log.d("oops", "Should work!");
            handleNewLocation(location);
        };
    }

    @Override
    public void onConnectionSuspended(int i) {
        Log.d("oops", "ConnectionSuspended");
    }

    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {
        Log.d("oops", "ConnectionFailed");
    }

    @Override
    public void onLocationChanged(Location location) {
        handleNewLocation(location);
    }
}
