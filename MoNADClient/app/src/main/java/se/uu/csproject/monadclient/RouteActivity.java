package se.uu.csproject.monadclient;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;


public class RouteActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //// TODO Ilyass: dynamically set the content view as the trip details (map probably not shown -TBD)
        setContentView(R.layout.activity_route);
        Toolbar toolbar = (Toolbar)findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        Button btn_join_trips = (Button)findViewById(R.id.btn_join_trips);
        btn_join_trips.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                Intent myIntent = new Intent(RouteActivity.this, RouteConfirmPopup.class);
                RouteActivity.this.startActivity(myIntent);


            }
        });

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
}
