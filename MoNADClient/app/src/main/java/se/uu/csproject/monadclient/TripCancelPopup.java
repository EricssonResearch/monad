package se.uu.csproject.monadclient;

import android.content.Intent;
import android.graphics.Color;
import android.os.CountDownTimer;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import java.text.DecimalFormat;

import se.uu.csproject.monadclient.recyclerviews.Trip;

import static java.lang.Math.floor;

public class TripCancelPopup extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.popup_trip_cancel);

        TextView startPosition = (TextView) findViewById(R.id.label_startposition);
        TextView endPosition = (TextView) findViewById(R.id.label_endposition);
        TextView startTime = (TextView) findViewById(R.id.label_starttime);
        TextView endTime = (TextView) findViewById(R.id.label_endtime);
        final TextView date = (TextView) findViewById(R.id.label_date);
        final TextView countdown = (TextView) findViewById(R.id.label_countdown);
        final ImageView clockIcon = (ImageView) findViewById(R.id.icon_clock);

        final Bundle b = getIntent().getExtras();
        Trip trip = new Trip(b.getInt("tripId"), b.getString("startPosition"),
                b.getString("endPosition"), b.getString("startTime"), b.getString("endTime"),
                b.getInt("duration"), b.getInt("feedback"));
        startPosition.setText(trip.getStartPosition());
        endPosition.setText(trip.getStartTime());
        startTime.setText(trip.getEndPosition());
        endTime.setText(trip.getEndTime());
        date.setText("TODAY");
        final long MILLISECONDS_TO_DEPARTURE = trip.getTimeToDeparture();
        countdown.setText(String.valueOf(MILLISECONDS_TO_DEPARTURE));

        //TODO (low priority): change parseColor() calls into theme colors
        final int MILLISECONDS = b.getInt("MILLISECONDS");
        CountDownTimer timer = new CountDownTimer(MILLISECONDS_TO_DEPARTURE, MILLISECONDS) {
            @Override
            public void onTick(long millisUntilFinished) {
                countdown.setText(formatCoundownText(millisUntilFinished));
                if (millisUntilFinished < 10000) {
                    countdown.setTextColor(Color.parseColor("#f44336"));
                    date.setTextColor(Color.parseColor("#f44336"));
                    clockIcon.setVisibility(View.VISIBLE);
                }
            }

            @Override
            public void onFinish() {
                countdown.setText("Trip in Progress");
                countdown.setTextColor(Color.parseColor("#2e7d32"));
                date.setTextColor(Color.parseColor("#2e7d32"));
                clockIcon.setVisibility(View.INVISIBLE);
                //clockIcon.setColorFilter(Color.parseColor("#2e7d32"));
            }
        }.start();

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        int width = dm.widthPixels;
        int height = dm.heightPixels;
        getWindow().setLayout((int) (width * .9), (int) (height * .38));
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
    //TODO Stavros: remove trip from user's schedule if the confirm button is clicked
    public void dropTrip(View view) {
        startActivity(new Intent(this, MainActivity.class));
    }

    public void backButtonClick(View view) {
        finish();
    }

    private String formatCoundownText(long millisecondsTime){
        DecimalFormat formatter = new DecimalFormat("00");
        String hours = formatter.format( floor(millisecondsTime / (1000 * 60 * 60)) );
        millisecondsTime %= (1000*60*60);
        String minutes = formatter.format( floor(millisecondsTime / (1000*60)) );
        millisecondsTime %= (1000*60);
        String seconds = formatter.format( floor(millisecondsTime / 1000) );
        return hours + ":" + minutes + ":" + seconds;
    }
}
