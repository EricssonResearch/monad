package se.uu.csproject.monadclient;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

import se.uu.csproject.monadclient.recyclerviews.SearchRecyclerViewAdapter;
import se.uu.csproject.monadclient.recyclerviews.Trip;

public class SearchActivity extends AppCompatActivity {
    private TextView textViewTripTimeDate;
    private TextView textViewTripTimeHour;
    private RadioButton arrivalTimeRadioButton;
    private RadioButton depatureTimeRadioButton;
    private RadioButton tripTimeButton;
    private RadioButton tripDistanceButton;
    private RadioGroup tripTimeRadioGroup;
    private RadioGroup priorityRadioGroup;
    private EditText positionEditText;
    private EditText destinationEditText;
    private Button searchButton;
    //private DatePicker datePicker;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search);
        Toolbar toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        arrivalTimeRadioButton = (RadioButton) findViewById(R.id.radiobutton_search_arrivaltime);
        depatureTimeRadioButton = (RadioButton) findViewById(R.id.radiobutton_search_departuretime);
        textViewTripTimeDate = (TextView) findViewById(R.id.textview_search_tripdatetime);
        textViewTripTimeHour = (TextView) findViewById(R.id.textview_search_triptimehour);

        tripTimeRadioGroup = (RadioGroup) findViewById(R.id.radiogroup_search_triptime);
        priorityRadioGroup = (RadioGroup) findViewById(R.id.radiogroup_search_priority);
        tripDistanceButton = (RadioButton) findViewById(R.id.radiobutton_search_prioritytriptime);
        tripTimeButton = (RadioButton) findViewById(R.id.radiobutton_search_prioritytripdistance);
        positionEditText = (EditText) findViewById(R.id.edittext_search_position);
        destinationEditText = (EditText) findViewById(R.id.edittext_search_destination);
        //datePicker = (DatePicker) findViewById(R.id.date_picker);

        searchButton = (Button) findViewById(R.id.button_search_search);

        RadioGroupListenerTime listenerTime = new RadioGroupListenerTime();
        tripTimeRadioGroup.setOnCheckedChangeListener(listenerTime);

        RadioGroupListenerPriority listenerPriority = new RadioGroupListenerPriority();
        priorityRadioGroup.setOnCheckedChangeListener(listenerPriority);

        tripTimeRadioGroup.check(depatureTimeRadioButton.getId());
        priorityRadioGroup.check(tripTimeButton.getId());

        List<Trip> searchResults = new ArrayList<>();
        RecyclerView recyclerView = (RecyclerView) findViewById(R.id.recycler_view_search);
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(getApplicationContext());
        recyclerView.setLayoutManager(linearLayoutManager);
        generateSearchResults(searchResults);
        SearchRecyclerViewAdapter adapter = new SearchRecyclerViewAdapter(searchResults);
        recyclerView.setAdapter(adapter);


        // Hide the keyboard when launch this activity
        this.getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);
    }

    // When the user touch somewhere else than focusable object, hide keyboard
    @Override
    public boolean onTouchEvent(MotionEvent event) {
        InputMethodManager imm = (InputMethodManager)getSystemService(Context.
                INPUT_METHOD_SERVICE);
        imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), 0);
        return true;
    }

    // Change the info if the priority button pressed dummy!
    class RadioGroupListenerPriority implements RadioGroup.OnCheckedChangeListener{
        //TODO: handle search results based on priority
        @Override
        public void onCheckedChanged(RadioGroup group, int checkedId) {
            if (checkedId == tripDistanceButton.getId()){

            }
            if (checkedId == tripTimeButton.getId()){


            }
        }
    }

    // Change the info if the depature/arrival button pressed  dummy!
    class RadioGroupListenerTime implements RadioGroup.OnCheckedChangeListener{

        @Override
        public void onCheckedChanged(RadioGroup group, int checkedId) {
            if (checkedId == arrivalTimeRadioButton.getId()){
                textViewTripTimeDate.setText("Thu, Nov, 9");
                textViewTripTimeHour.setText("21:20, AM");
            }
            if (checkedId == depatureTimeRadioButton.getId()){
                textViewTripTimeDate.setText("Fri, Oct, 2");
                textViewTripTimeHour.setText("11:45, AM");
            }
        }
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
            //TODO: Create a toaster with text about the MoNAD project and team
            startActivity(new Intent(this, AboutUsActivity.class));
        }

        if (id == R.id.action_signout) {
            startActivity(new Intent(this, LoginActivity.class));
        }

        return super.onOptionsItemSelected(item);
    }

    public void openTripDetail (View v) {
        startActivity(new Intent(this, RouteActivity.class));
    }

    public void sendTravelRequest (View v) {
        new SendTravelRequest().execute();
    }

    //TEMPORARY FUNCTION TODO: Remove this function once the database connection is set
    private void generateSearchResults(List<Trip> trips){
        trips.add(new Trip(1, "Polacksbacken","12:36","Flogsta", "12:51", 15, 2));
        trips.add(new Trip(2, "Polacksbacken","20:36","Flogsta", "20:51", 15, 4));
        trips.add(new Trip(3, "Gamla Uppsala","19:17","Övre Slottsgatan", "19:35", 18, 3));
        trips.add(new Trip(4, "Polacksbacken", "12:36", "Flogsta", "12:51", 15, 0));
    }
}
