package se.uu.csproject.monadclient;

import android.Manifest;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Build;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.NavUtils;
import android.support.v4.content.ContextCompat;
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
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.List;
import java.util.Locale;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.PartialTrip;
import se.uu.csproject.monadclient.recyclerviews.RecommendedTrips;
import se.uu.csproject.monadclient.recyclerviews.SearchRecyclerViewAdapter;

public class MainActivity extends MenuedActivity implements
        GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener, LocationListener {

    private EditText destination;
    private GoogleApiClient mGoogleApiClient;
    private LocationRequest mLocationRequest;
    private double currentLatitude;
    private double currentLongitude;
    private final int MY_PERMISSIONS_REQUEST = 123;
    private Context context;

    //Google Cloud Services
    private static final String TAG = "MainActivity";
    private static final int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        destination = (EditText) findViewById(R.id.main_search_destination);
        setSupportActionBar(toolbar);

        context = getApplicationContext();
        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        List<FullTrip> searchResults = new ArrayList<>();
        RecyclerView recyclerView = (RecyclerView) findViewById(R.id.recycler_view_main);
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(getApplicationContext());
        recyclerView.setLayoutManager(linearLayoutManager);
        generateSearchResults(searchResults);
        SearchRecyclerViewAdapter adapter = new SearchRecyclerViewAdapter(searchResults);
        recyclerView.setAdapter(adapter);
        buildGoogleApiClient();
        initializeLocationRequest();

        if (Build.VERSION.SDK_INT >= 23) {
            checkForPermission();
        } else {
            mGoogleApiClient.connect();
        }
    }

    public void openMainSearch (View view) {
        // Make a quick search based on the current time and the user's current location
        String startPositionLatitude, startPositionLongitude, edPosition, userId, startTime, endTime;
        String requestTime, priority;
        Date now = new Date();
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.ENGLISH);

        // Provide some default values since this is a quick search
        startPositionLatitude = String.valueOf(currentLatitude);
        startPositionLongitude = String.valueOf(currentLongitude);
        edPosition = destination.getText().toString();
        userId = ClientAuthentication.getClientId();
        startTime = df.format(now);
        endTime = "null";
        requestTime = df.format(now);
        priority = "distance";

        if(edPosition != null && !edPosition.trim().isEmpty()){
            SendQuickTravelRequest asyncTask = new SendQuickTravelRequest();
            asyncTask.delegate = this;
            asyncTask.execute(userId, startTime, endTime, requestTime, startPositionLatitude,
                    startPositionLongitude, edPosition, priority);
        } else {
            Context context = getApplicationContext();
            CharSequence text = "Please enter a destination address.";
            int duration = Toast.LENGTH_SHORT;

            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }
    }

    public void processFinish(ArrayList<FullTrip> searchResults){

        if (searchResults.isEmpty()){
            CharSequence text = "Could not find any trips matching your criteria.";
            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }

        Intent myIntent = new Intent(MainActivity.this, SearchActivity.class);
        RecommendedTrips recommendedTrips = new RecommendedTrips(searchResults);
        myIntent.putExtra("searchResults", recommendedTrips);
        MainActivity.this.startActivity(myIntent);
    }

    private void checkForPermission(){
        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(MainActivity.this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, MY_PERMISSIONS_REQUEST);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSIONS_REQUEST: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    mGoogleApiClient.connect();
                } else {
                    // Permission denied, boo! Disable the functionality that depends on this permission.
                    Context context = getApplicationContext();
                    CharSequence text = "If you don't give location permission then the quick search " +
                                        "will not work correctly";
                    int duration = Toast.LENGTH_LONG;

                    Toast toast = Toast.makeText(context, text, duration);
                    toast.show();
                }
                return;
            }
        }
    }

    private void handleNewLocation(Location location) {
        currentLatitude = location.getLatitude();
        currentLongitude = location.getLongitude();
    }

    protected synchronized void buildGoogleApiClient() {
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(LocationServices.API)
                .build();
    }

    protected void initializeLocationRequest() {
        mLocationRequest = LocationRequest.create()
                .setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY)
                .setInterval(60 * 1000)        // 1 minute, in milliseconds
                .setFastestInterval(10 * 1000); // 10 seconds, in milliseconds
    }

//    @Override
//    public boolean onCreateOptionsMenu(Menu menu) {
//
//        if(ClientAuthentication.getPassword().equals("0")){
//        // Inflate the menu; this adds items to the action bar if it is present.
//        getMenuInflater().inflate(R.menu.menu_main_google, menu);
//        return true;
//        }
//        else {
//            getMenuInflater().inflate(R.menu.menu_main, menu);
//            return true;
//        }
//    }

    public boolean onTouchEvent(MotionEvent event) {
        InputMethodManager imm = (InputMethodManager)getSystemService(Context.
                INPUT_METHOD_SERVICE);
        imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), 0);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if(id == R.id.action_search){
            return true;
        }
        else {
            return super.onOptionsItemSelected(item);
        }
    }

    public void openTripDetail (View v) {
        //opens Route activity layout
        startActivity(new Intent(this, RouteActivity.class));
    }

    //TEMPORARY FUNCTION TODO: Remove this function once the database connection is set
    private void generateSearchResults(List<FullTrip> trips){
        Calendar calendar = new GregorianCalendar(2015, 10, 26, 10, 40, 0);
        Date startdate1 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 26, 10, 50, 0);
        Date enddate1 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 26, 10, 45, 0);
        Date startdate2 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 26, 11, 0, 0);
        Date enddate2 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 27, 9, 50, 0);
        Date startdate3 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 27, 10, 5, 0);
        Date enddate3 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 22, 11, 30, 0);
        Date startdate4 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 10, 22, 12, 0, 0);
        Date enddate4 = calendar.getTime();

        ArrayList<PartialTrip> partialTrips = new ArrayList<>();
        ArrayList<String> trajectory = new ArrayList<>();
        trajectory.add("BMC");
        trajectory.add("Akademiska Sjukhuset");
        trajectory.add("Ekeby Bruk");
        trajectory.add("Ekeby");
        partialTrips.add(new PartialTrip(1, "Polacksbacken",startdate1,"Flogsta", enddate1, trajectory));
        trips.add(new FullTrip("1", "2", partialTrips, 10, false, 0));
        partialTrips.clear(); partialTrips.add(new PartialTrip(2, "Gamla Uppsala",startdate2,"Gottsunda", enddate2, trajectory));
        trips.add(new FullTrip("2", "3", partialTrips, 15, false, 0));
        partialTrips.clear(); partialTrips.add(new PartialTrip(3, "Granby",startdate3,"Tunna Backar", enddate3, trajectory));
        trips.add(new FullTrip("3", "4", partialTrips, 15, false, 0));
        partialTrips.clear(); partialTrips.add(new PartialTrip(4, "Kungsgatan", startdate4, "Observatoriet", enddate4, trajectory));
        trips.add(new FullTrip("4", "5", partialTrips, 30, false, 0));
    }

    @Override
    protected void onResume() {
        super.onResume();

        boolean finish = getIntent().getBooleanExtra("FINISH", false);
        //Log.i("FINISH-NEWINTENT", finish + "");
        if (finish) {
            startActivity(new Intent(MainActivity.this, LoginActivity.class));
            finish();
        }

        if (!mGoogleApiClient.isConnected()) {
            if (Build.VERSION.SDK_INT >= 23){
                checkForPermission();
            } else {
                mGoogleApiClient.connect();
            }
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        /*if (mGoogleApiClient.isConnected()) {
            LocationServices.FusedLocationApi.removeLocationUpdates(mGoogleApiClient, this);
            mGoogleApiClient.disconnect();
        }*/
    }

    //TODO (Huijie): prompt the user to choose before leaving the application
    @Override
    public void onBackPressed() {
        /*
        if(isTaskRoot()){
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            // Add the buttons
            builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    // User clicked OK button
                    MainActivity.super.onBackPressed();
                    Toast.makeText(getApplicationContext(), "You have exited MoNAD.", Toast.LENGTH_LONG).show();
                }
            });
            builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    // User cancelled the dialog
                    //do nothing
                }
            });
            // Create the AlertDialog
            AlertDialog dialog = builder.create();
            dialog.show();
        }
        */
    }

    @Override
    public void onConnected(Bundle bundle) {
        Location location = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);

        if (location == null) {
            // This exception will be thrown on android 6 devices where the user hasn't given location permission
            try{
                LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient, mLocationRequest, this);
            }catch(java.lang.SecurityException e){
                Log.d("oops", e.toString());
            }
        }
        else {
            handleNewLocation(location);
        }
    }

    @Override
    public void onConnectionSuspended(int i) {

    }

    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {
        Log.d("oops", "Connection failed with error code: " + Integer.toString(connectionResult.getErrorCode()));
    }

    @Override
    public void onLocationChanged(Location location) {
        handleNewLocation(location);
    }


    private boolean checkPlayServices() {

        GoogleApiAvailability apiAvailability = GoogleApiAvailability.getInstance();
        int resultCode = apiAvailability.isGooglePlayServicesAvailable(this);
        if (resultCode != ConnectionResult.SUCCESS) {
            if (apiAvailability.isUserResolvableError(resultCode)) {
                apiAvailability.getErrorDialog(this, resultCode, PLAY_SERVICES_RESOLUTION_REQUEST)
                        .show();
            } else {
                Log.i(TAG, "This device is not supported.");
                finish();
            }
            return false;
        }
        return true;
    }

}
