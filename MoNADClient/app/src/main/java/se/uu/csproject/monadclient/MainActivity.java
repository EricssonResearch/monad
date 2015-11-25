package se.uu.csproject.monadclient;

import android.Manifest;
import android.app.AlarmManager;
import android.app.AlertDialog;
import android.app.PendingIntent;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.location.Location;
import android.os.AsyncTask;
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
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Locale;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.SearchRecyclerViewAdapter;
import se.uu.csproject.monadclient.recyclerviews.Storage;

public class MainActivity extends MenuedActivity implements GoogleApiClient.ConnectionCallbacks,
        GoogleApiClient.OnConnectionFailedListener, LocationListener, AsyncResponse, AsyncRecommendationsInteraction {

    private AutoCompleteTextView destination;
    private GoogleApiClient mGoogleApiClient;
    private LocationRequest mLocationRequest;
    private double currentLatitude, currentLongitude;
    private Context context;
    private Toolbar toolbar;
    private AlertDialog.Builder builder;
    private RecyclerView recyclerView;
    private SearchRecyclerViewAdapter adapter;

    private static final int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;
    private final int MY_PERMISSIONS_REQUEST = 123;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Locale locale = new Locale(ClientAuthentication.getLanguage());
        Locale.setDefault(locale);
        Configuration config = new Configuration();
        config.locale = locale;
        getBaseContext().getResources().updateConfiguration(config,
                getBaseContext().getResources().getDisplayMetrics());
        setContentView(R.layout.activity_main);
        initAlertDialog();

        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        destination = (AutoCompleteTextView) findViewById(R.id.main_search_destination);
        context = getApplicationContext();
        currentLatitude = 0;
        currentLongitude = 0;
        setSupportActionBar(toolbar);

        recyclerView = (RecyclerView) findViewById(R.id.recycler_view_main);
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(getBaseContext());
        recyclerView.setLayoutManager(linearLayoutManager);

        buildGoogleApiClient();
        initializeLocationRequest();
        String[] addresses = getAddressesFromFileAsset();

        if (addresses != null){
            ArrayAdapter<String> adapterString =
                    new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, addresses);
            destination.setAdapter(adapterString);
        }

        // Hide the keyboard when launching this activity
        this.getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);
    }

    public String[] getAddressesFromFileAsset(){
        String[] addresses = null;
        ArrayList<String> addressesList = new ArrayList<>();
        String line;

        try{
            BufferedReader reader = new BufferedReader(new InputStreamReader(getAssets().open("addresses.txt")));
            while ((line = reader.readLine()) != null) {
                addressesList.add(line);
            }
            addresses = new String[addressesList.size()];
            addresses = addressesList.toArray(addresses);
        }
        catch (IOException e) {
            Log.d("oops", e.toString());
        }

        return addresses;
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
            CharSequence text = getString(R.string.java_search_enterdestination);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    // Deals with the response by the server
    public void processFinish(ArrayList<FullTrip> searchResults){
        if (searchResults.isEmpty()){
            CharSequence text = getString(R.string.java_main_noresults);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
            toast.show();
            Storage.clearSearchResults();
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
                    CharSequence text = getString(R.string.java_locationpermissionwarning);
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
        Storage.clearSearchResults();
        startActivity(new Intent(this, SearchActivity.class));
    }

    @Override
    protected void onResume() {
        super.onResume();

        boolean finish = getIntent().getBooleanExtra("FINISH", false);
        if (finish) {
            //clear user profile
            ClientAuthentication.initProfile();
            Storage.clearAll();
            startActivity(new Intent(MainActivity.this, LoginActivity.class));
            finish();
        }

        /* GetRecommendations */
        if (!Storage.isEmptyRecommendations()) {
            displayRecommendations();
        }
        else {
            getRecommendations();
        }

        /* TODO: GetNotifications */
//        new NotificationsInteraction("MainActivity").getNotifications();

        if (checkPlayServices()){
            if (!mGoogleApiClient.isConnected()) {
                if (Build.VERSION.SDK_INT >= 23){
                    checkForPermission();
                } else {
                    mGoogleApiClient.connect();
                }
            }
        } else {
            CharSequence text = getString(R.string.java_googleplaywarning);
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

    private void initAlertDialog(){
        builder = new AlertDialog.Builder(this);
        builder.setTitle(getString(R.string.java_confirm));
        builder.setMessage(getString(R.string.java_main_exitmonad));
        // Add the buttons
        builder.setPositiveButton(getString(R.string.java_yes), new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int id) {
                // User clicked Yes button
                MainActivity.super.onBackPressed();
                Toast.makeText(getApplicationContext(), getString(R.string.java_main_leftmonad), Toast.LENGTH_LONG).show();
            }
        });
        builder.setNegativeButton(getString(R.string.java_cancel), new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int id) {
                // User cancelled the dialog
                //do nothing
            }
        });
    }

    /* Prompt the user to confirm if he/she wants to exit MoNAD or not if this is the root task in the back stack */
    /* Don't need to check if it's the root task. This is because after mainActivity finish,
     * all the activities below it in the back stack are destroyed right away (e.g. in the case of google login) */
    @Override
    public void onBackPressed() {
        // Create the AlertDialog
        AlertDialog dialog = builder.create();
        dialog.show();
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

    public void getRecommendations() {
        new GetRecommendationsTask(this).executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
    }

    @Override
    public void processReceivedRecommendations() {
        displayRecommendations();

        //add to notify
        Intent myIntent = new Intent(MainActivity.this, RecommendationAlarmReceiver.class);
        PendingIntent pendingIntent = PendingIntent.getBroadcast(MainActivity.this, 0, myIntent, 0);

        AlarmManager am = (AlarmManager) getSystemService(Context.ALARM_SERVICE);
//
//        Calendar calendar = Calendar.getInstance();
//        calendar.setTimeInMillis(System.currentTimeMillis());
//        calendar.set(Calendar.HOUR_OF_DAY, 16);
//        calendar.set(Calendar.MINUTE, 0);

        am.set(AlarmManager.RTC_WAKEUP, System.currentTimeMillis() + 5000, pendingIntent);

    }

    public void displayRecommendations() {
        adapter = new SearchRecyclerViewAdapter(Storage.getRecommendations());
        recyclerView.setAdapter(adapter);
    }
}
