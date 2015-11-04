package se.uu.csproject.monadclient;

import android.content.Intent;
import android.os.CountDownTimer;
import android.support.v4.app.NavUtils;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;

import java.text.DecimalFormat;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;

import static java.lang.Math.floor;

public class RouteSuccessActivity extends AppCompatActivity {

    Toolbar toolbar;
    FullTrip trip;
    TextView countdownTime;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_route_success);
        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        countdownTime = (TextView) findViewById(R.id.label_countdown);
        Bundle b = getIntent().getExtras();
        trip = b.getParcelable("selectedTrip");

        final long MILLISECONDS = 1000;
        final long MILLISECONDS_TO_DEPARTURE = trip.getTimeToDeparture();
        countdownTime.setText(formatCountdownText(MILLISECONDS_TO_DEPARTURE));

        CountDownTimer timer = new CountDownTimer(MILLISECONDS_TO_DEPARTURE, MILLISECONDS) {
            @Override
            public void onTick(long millisUntilFinished) {
                countdownTime.setText(formatCountdownText(millisUntilFinished));
                //change value to 30min (30*60*1000 = 1 800 000ms)
                if (millisUntilFinished < 1800000) {
                    countdownTime.setTextColor(ContextCompat.getColor(countdownTime.getContext(), R.color.warnColor));
                }
            }

            @Override
            public void onFinish() {
                countdownTime.setText("Trip in Progress");
                countdownTime.setTextColor(ContextCompat.getColor(countdownTime.getContext(), R.color.green));
            }
        }.start();
    }

    private String formatCountdownText(long millisecondsTime){
        DecimalFormat formatter = new DecimalFormat("00");
        String days = formatter.format(floor(millisecondsTime / (1000 * 60 * 60 * 24)));
        millisecondsTime %= (1000*60*60*24);
        String hours = formatter.format( floor(millisecondsTime / (1000 * 60 * 60)) );
        millisecondsTime %= (1000*60*60);
        String minutes = formatter.format(floor(millisecondsTime / (1000 * 60)));
        millisecondsTime %= (1000*60);
        String seconds = formatter.format(floor(millisecondsTime / 1000));
        if(days.equals("00")){
            return hours + ":" + minutes + ":" + seconds;
        }
        else if(days.equals("01")){
            return days + " day, " + hours + ":" + minutes + ":" + seconds;
        }
        else{
            return days + " day(s), " + hours + ":" + minutes + ":" + seconds;
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

        if(id == android.R.id.home) {
            NavUtils.navigateUpFromSameTask(this);
        }

        if (id == R.id.action_search) {
            startActivity(new Intent(this, MainActivity.class));
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
        }

        if (id == R.id.action_signout) {
            startActivity(new Intent(this, LoginActivity.class));
        }

        return super.onOptionsItemSelected(item);
    }

    public void linkToTripDetails(View view) {
        startActivity(new Intent(this, RouteActivity.class));
        finish();
    }

    public void linkToSearch(View view){
        startActivity(new Intent(this, MainActivity.class));
        finish();
    }
}
