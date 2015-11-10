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
import android.support.v4.content.ContextCompat;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
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
import java.util.concurrent.ExecutionException;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.PartialTrip;
import se.uu.csproject.monadclient.recyclerviews.SearchRecyclerViewAdapter;
import se.uu.csproject.monadclient.recyclerviews.Storage;

public class MainActivity extends MenuedActivity implements
        GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener, LocationListener, AsyncResponse {

    private EditText destination;
    private GoogleApiClient mGoogleApiClient;
    private LocationRequest mLocationRequest;
    private double currentLatitude, currentLongitude;
    private Context context;
    private Toolbar toolbar;

    private static final int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;
    private final int MY_PERMISSIONS_REQUEST = 123;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        destination = (EditText) findViewById(R.id.main_search_destination);
        context = getApplicationContext();
        currentLatitude = 0;
        currentLongitude = 0;
        setSupportActionBar(toolbar);
        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        List<FullTrip> searchResults = new ArrayList<>();
        RecyclerView recyclerView = (RecyclerView) findViewById(R.id.recycler_view_main);
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(getApplicationContext());
        recyclerView.setLayoutManager(linearLayoutManager);

        /* TODO: Routes Generation (Please ignore that) */
//        RoutesGenerationTask rt = new RoutesGenerationTask();
//        rt.execute();

        /* TODO: GetRecommendations */
//        System.out.println(ClientAuthentication.profileToString());

//        GetRecommendationsTask recommendationsTask = new GetRecommendationsTask();
//        try {
//            String response = recommendationsTask.execute().get();
//
//            Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();
//
//            // If the response starts with the specific word, it means the users logged in successfully
//            if (response.startsWith("Success (1)")) {
//                System.out.println("________________OK________________");
//            }
//            else {
//                System.out.println("________________NOT OK________________");
//            }
//        } catch (InterruptedException e) {
//            e.printStackTrace();
//        } catch (ExecutionException e) {
//            e.printStackTrace();
//        }

        generateSearchResults(searchResults);
        SearchRecyclerViewAdapter adapter = new SearchRecyclerViewAdapter(searchResults);
        recyclerView.setAdapter(adapter);

        buildGoogleApiClient();
        initializeLocationRequest();

        // Hide the keyboard when launching this activity
        this.getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);
    }

    // Called when the user clicks on the quick search button
    public void openMainSearch (View view) {
        String startPositionLatitude, startPositionLongitude, edPosition, userId, startTime, endTime;
        String requestTime, priority;
        Date now = new Date();
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.ENGLISH);

        startPositionLatitude = String.valueOf(currentLatitude);
        startPositionLongitude = String.valueOf(currentLongitude);
        edPosition = destination.getText().toString();
        userId = ClientAuthentication.getClientId();
        startTime = df.format(now);
        requestTime = df.format(now);
        endTime = "null";
        priority = "distance";

        if(edPosition != null && !edPosition.trim().isEmpty()){
            SendQuickTravelRequest asyncTask = new SendQuickTravelRequest();
            asyncTask.delegate = this;
            asyncTask.execute(userId, startTime, endTime, requestTime, startPositionLatitude,
                    startPositionLongitude, edPosition, priority);
        } else {
            CharSequence text = "Please enter a destination address.";
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    // Deals with the response by the server
    public void processFinish(ArrayList<FullTrip> searchResults){
        if (searchResults.isEmpty()){
            CharSequence text = "Could not find any trips matching your criteria, try using the advanced search.";
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
            toast.show();
            Storage.clearAll();
        }
        Intent myIntent = new Intent(MainActivity.this, SearchActivity.class);
        myIntent.putExtra("destination", destination.getText().toString());
        MainActivity.this.startActivity(myIntent);
    }

    // Checks if the user has given location permission and asks for it if he hasn't
    private void checkForPermission(){
        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(MainActivity.this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, MY_PERMISSIONS_REQUEST);
        } else {
            mGoogleApiClient.connect();
        }
    }

    // Checks the result of the permission asked of the user
    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSIONS_REQUEST: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    mGoogleApiClient.connect();
                } else {
                    // Permission denied, boo! Disable the functionality that depends on this permission.
                    CharSequence text = "If you don't give location permission then we can't use " +
                            "your current location to search for suitable bus trips.";
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

    public void goToAdvancedSearch(View v) {
        Storage.clearAll();
        startActivity(new Intent(this, SearchActivity.class));
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
        partialTrips.add(new PartialTrip("1", 2, 3, "Polacksbacken",startdate1,"Flogsta", enddate1, trajectory));
        trips.add(new FullTrip("1", "2", partialTrips, 10, true, 0));
        partialTrips.clear(); partialTrips.add(new PartialTrip("1", 2, 3, "Gamla Uppsala", startdate2, "Gottsunda", enddate2, trajectory));
        trips.add(new FullTrip("2", "3", partialTrips, 15, true, 0));
        partialTrips.clear(); partialTrips.add(new PartialTrip("1",2,3, "Granby",startdate3,"Tunna Backar", enddate3, trajectory));
        trips.add(new FullTrip("3", "4", partialTrips, 15, true, 0));
        partialTrips.clear(); partialTrips.add(new PartialTrip("1",2,3, "Kungsgatan", startdate4, "Observatoriet", enddate4, trajectory));
        trips.add(new FullTrip("4", "5", partialTrips, 30, true, 0));
    }

    @Override
    protected void onResume() {
        super.onResume();

        boolean finish = getIntent().getBooleanExtra("FINISH", false);
        if (finish) {
            //clear user profile
            ClientAuthentication.initProfile();
            startActivity(new Intent(MainActivity.this, LoginActivity.class));
            finish();
        }

        if (checkPlayServices()){
            if (!mGoogleApiClient.isConnected()) {
                if (Build.VERSION.SDK_INT >= 23){
                    checkForPermission();
                } else {
                    mGoogleApiClient.connect();
                }
            }
        } else {
            CharSequence text = "If you don't have google play services enabled then we can't use " +
                    "your current location to search for suitable bus trips.";
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_LONG);
            toast.show();
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (mGoogleApiClient.isConnected()) {
            LocationServices.FusedLocationApi.removeLocationUpdates(mGoogleApiClient, this);
            mGoogleApiClient.disconnect();
        }
    }

    /* Prompt the user to confirm if he/she wants to exit MoNAD or not if this is the root task in the back stack */
    @Override
    public void onBackPressed() {
        if(isTaskRoot()){
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("Confirm");
            builder.setMessage("Do you want to exit MoNAD?");
            // Add the buttons
            builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    // User cancelled the dialog
                    //do nothing
                }
            });
            builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    // User clicked OK button
                    MainActivity.super.onBackPressed();
                    Toast.makeText(getApplicationContext(), "You have exited MoNAD.", Toast.LENGTH_LONG).show();
                }
            });
            // Create the AlertDialog
            AlertDialog dialog = builder.create();
            dialog.show();
        }
    }

    @Override
    public void onConnected(Bundle bundle) {
        Location location = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);

        if (location == null) {
            LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient, mLocationRequest, this);
        } else {
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

    // Checks if the user has google play services enabled
    private boolean checkPlayServices() {
        GoogleApiAvailability apiAvailability = GoogleApiAvailability.getInstance();
        int resultCode = apiAvailability.isGooglePlayServicesAvailable(this);
        if (resultCode != ConnectionResult.SUCCESS) {
            if (apiAvailability.isUserResolvableError(resultCode)) {
                apiAvailability.getErrorDialog(this, resultCode, PLAY_SERVICES_RESOLUTION_REQUEST).show();
            }
            return false;
        }
        return true;
    }
}
