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
import android.net.Uri;
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

public class MainActivity extends MenuedActivity implements AsyncResponse, AsyncRecommendationsInteraction {

    private AutoCompleteTextView destination;
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
        setSupportActionBar(toolbar);

        recyclerView = (RecyclerView) findViewById(R.id.recycler_view_main);
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(getBaseContext());
        recyclerView.setLayoutManager(linearLayoutManager);

        if (!getIntent().getBooleanExtra("FINISH", false)){
            // Start the location service if the user has given permission
            if (checkPlayServices()){
                if (Build.VERSION.SDK_INT >= 23){
                    checkForPermission();
                } else {
                    startService(new Intent(this, LocationService.class));
                }
            } else {
                CharSequence text = getString(R.string.java_googleplaywarning);
                Toast toast = Toast.makeText(context, text, Toast.LENGTH_LONG);
                toast.show();
            }
        }

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

        startPositionLatitude = String.valueOf(Storage.getLatitude());
        startPositionLongitude = String.valueOf(Storage.getLongitude());
        edPosition = destination.getText().toString();
        userId = ClientAuthentication.getClientId();
        startTime = df.format(now);
        requestTime = df.format(now);
        endTime = "null";
        priority = "distance";

        if (edPosition != null && !edPosition.trim().isEmpty() &&
                Storage.getLatitude() != 0.0 && Storage.getLongitude() != 0.0){
            SendQuickTravelRequest asyncTask = new SendQuickTravelRequest();
            asyncTask.delegate = this;
            asyncTask.execute(userId, startTime, endTime, requestTime, startPositionLatitude,
                    startPositionLongitude, edPosition, priority);
        } else if (edPosition == null || edPosition.trim().isEmpty()){
            CharSequence text = getString(R.string.java_search_enterdestination);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
            toast.show();
        } else {
            CharSequence text = getString(R.string.java_search_locationdisabled);
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
            startService(new Intent(this, LocationService.class));
        }
    }

    // Checks the result of the permission asked of the user
    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSIONS_REQUEST: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    startService(new Intent(this, LocationService.class));
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
            ClientAuthentication.clearGlobalVariables();

            //clear trip, recommendations, etc.
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
    }

    @Override
    protected void onPause() {
        super.onPause();
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

        if(!ClientAuthentication.getIfRecommendNotifyAdded()) {
            //add to notify
            ArrayList<FullTrip> recommendations = Storage.getRecommendations();

            int i = 1;

            for(FullTrip ft:recommendations) {
                Intent myIntent = new Intent(MainActivity.this, RecommendationAlarmReceiver.class);
                myIntent.setData(Uri.parse("timer:"+i));
                myIntent.putExtra("selectedTrip", ft);

                PendingIntent pendingIntent = PendingIntent.getBroadcast(MainActivity.this, 0, myIntent, 0);

                AlarmManager am = (AlarmManager) getSystemService(Context.ALARM_SERVICE);

                //notify the user half an hour before the beginning of the trip
                am.set(AlarmManager.RTC_WAKEUP, ft.getStartTime().getTime() - 1800000, pendingIntent);

                ClientAuthentication.setIfRecommendNotifyAdded(true);

                i++;
            }
        }
    }

    public void displayRecommendations() {
        adapter = new SearchRecyclerViewAdapter(Storage.getRecommendations());
        recyclerView.setAdapter(adapter);
    }
}
