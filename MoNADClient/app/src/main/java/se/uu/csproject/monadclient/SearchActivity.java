package se.uu.csproject.monadclient;

import android.app.DatePickerDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.app.TimePickerDialog;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.text.format.DateFormat;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.TimePicker;
import android.widget.Toast;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import se.uu.csproject.monadclient.recyclerviews.SearchRecyclerViewAdapter;
import se.uu.csproject.monadclient.recyclerviews.Trip;

public class SearchActivity extends AppCompatActivity {
    private TextView textViewTripDate;
    DialogFragment dateFragment;
    private TextView textViewTripTime;
    DialogFragment timeFragment;
    private RadioButton arrivalTimeRadioButton;
    private RadioButton depatureTimeRadioButton;
    private RadioButton tripTimeButton;
    private RadioButton tripDistanceButton;
    private RadioGroup tripTimeRadioGroup;
    private RadioGroup priorityRadioGroup;
    private EditText positionEditText;
    private EditText destinationEditText;
    private Button searchButton;
    public Calendar calendar;
    static final int DIALOG_ID = 0;
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
        textViewTripDate = (TextView) findViewById(R.id.textview_search_tripdate);
        calendar = Calendar.getInstance();
        updateDate();
        textViewTripTime= (TextView) findViewById(R.id.textview_search_triptime);
        updateTime();

        textViewTripDate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showDatePickerDialog(v);
            }
        });
        textViewTripTime.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showTimePickerDialog(v);
            }
        });

        tripTimeRadioGroup = (RadioGroup) findViewById(R.id.radiogroup_search_triptime);
        priorityRadioGroup = (RadioGroup) findViewById(R.id.radiogroup_search_priority);
        tripDistanceButton = (RadioButton) findViewById(R.id.radiobutton_search_prioritytriptime);
        tripTimeButton = (RadioButton) findViewById(R.id.radiobutton_search_prioritytripdistance);
        positionEditText = (EditText) findViewById(R.id.edittext_search_position);
        destinationEditText = (EditText) findViewById(R.id.edittext_search_destination);

        searchButton = (Button) findViewById(R.id.button_search_search);

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

    public void showDatePickerDialog(View v) {
        dateFragment = new DatePickerFragment();
        dateFragment.show(getFragmentManager(), "datePicker");
    }

    public void showTimePickerDialog(View v) {
        timeFragment = new TimePickerFragment();
        timeFragment.show(getFragmentManager(), "timePicker");
    }

    public void updateDate() {
        final String DATE_FORMAT = "EEE dd MMM";
        SimpleDateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT);
        String selectedDate = dateFormat.format(calendar.getTime());
        textViewTripDate.setText(selectedDate);
    }

    public void updateTime() {
        final String TIME_FORMAT = "HH:mm";
        SimpleDateFormat timeFormat = new SimpleDateFormat(TIME_FORMAT);
        String selectedTime = timeFormat.format(calendar.getTime());
        textViewTripTime.setText(selectedTime);
    }

    public class DatePickerFragment extends DialogFragment implements DatePickerDialog.OnDateSetListener {
        @Override
        public Dialog onCreateDialog(Bundle savedInstanceState) {
            final Calendar c = Calendar.getInstance();
            int year = c.get(Calendar.YEAR);
            int month = c.get(Calendar.MONTH);
            int day = c.get(Calendar.DAY_OF_MONTH);
            return new DatePickerDialog(getActivity(), this, year, month, day);
        }

        public void onDateSet(DatePicker view, int year, int month, int day) {
            calendar.set(Calendar.YEAR, year);
            calendar.set(Calendar.MONTH, month);
            calendar.set(Calendar.DAY_OF_MONTH, day);
            updateDate();
        }
    }

    public class TimePickerFragment extends DialogFragment implements TimePickerDialog.OnTimeSetListener {

        @Override
        public Dialog onCreateDialog(Bundle savedInstanceState) {
            // Use the current time as the default values for the picker
            final Calendar c = Calendar.getInstance();
            int hour = c.get(Calendar.HOUR_OF_DAY);
            int minute = c.get(Calendar.MINUTE);

            // Create a new instance of TimePickerDialog and return it
            return new TimePickerDialog(getActivity(), this, hour, minute,
                    DateFormat.is24HourFormat(getActivity()));
        }

        public void onTimeSet(TimePicker view, int hourOfDay, int minute) {
            calendar.set(Calendar.HOUR_OF_DAY, hourOfDay);
            calendar.set(Calendar.MINUTE, minute);
            updateTime();
        }
    }

    // When the user touch somewhere else than focusable object, hide keyboard
    @Override
    public boolean onTouchEvent(MotionEvent event) {
        InputMethodManager imm = (InputMethodManager)getSystemService(Context.
                INPUT_METHOD_SERVICE);
        imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), 0);
        return true;
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
            //TODO (low priority): Create a toaster with text about the MoNAD project and team
            startActivity(new Intent(this, AboutUsActivity.class));
        }

        if (id == R.id.action_signout) {
            startActivity(new Intent(this, LoginActivity.class));
        }

        return super.onOptionsItemSelected(item);
    }

    public void openTripDetail(View v) {
        startActivity(new Intent(this, RouteActivity.class));
    }

    public void sendTravelRequest (View v) {
        //// TODO Stavros: retrieve various fields from the UI and send them to SendTravelRequest

        String stPosition, edPosition, userId, startTime, endTime, requestTime;
        int selectedId, currentYear;

        Date now = new Date();
        Calendar rightNow = Calendar.getInstance();
        currentYear = rightNow.get(Calendar.YEAR);
        SimpleDateFormat df = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
        startTime = "null";
        endTime = "null";
        requestTime = df.format(now);
        userId = ClientAuthentication.getClientId();
        stPosition = positionEditText.getText().toString();
        edPosition = destinationEditText.getText().toString();
        selectedId = tripTimeRadioGroup.getCheckedRadioButtonId();

        switch(selectedId){
            case R.id.radiobutton_search_departuretime:
                startTime = Integer.toString(currentYear) + " " + textViewTripDate.getText().toString() + " "
                        + textViewTripTime.getText().toString();
                break;

            case R.id.radiobutton_search_arrivaltime:
                endTime = Integer.toString(currentYear) + " " + textViewTripDate.getText().toString() + " "
                        + textViewTripTime.getText().toString();
                break;
        }

        new SendTravelRequest().execute(userId, startTime, endTime, requestTime, stPosition, edPosition);
    }

    //TEMPORARY FUNCTION TODO: Remove this function once the database connection is set
    private void generateSearchResults(List<Trip> trips){
        trips.add(new Trip(1, "Polacksbacken","12:36","Flogsta", "12:51", 15, 2));
        trips.add(new Trip(2, "Polacksbacken","20:36","Flogsta", "20:51", 15, 4));
        trips.add(new Trip(3, "Polacksbacken","19:17","Ekeby", "19:35", 18, 3));
        trips.add(new Trip(4, "Polacksbacken", "12:36", "Flogsta", "12:51", 15, 0));
    }
}
