package se.uu.csproject.monadclient;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.DisplayMetrics;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;

public class RouteConfirmPopup extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.popup_route_confirm);

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        int width = dm.widthPixels;
        int height = dm.heightPixels;
        getWindow().setLayout((int)(width*.9),(int)(height*.40));

        ImageButton cancel = (ImageButton)findViewById(R.id.cancelbutton);
        cancel.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {

                //return to the previous activity instead of start a new one
                finish();
                

            }


        });

        //TODO Stavros: store trip in user's schedule when button clicked
        Button button_confirm = (Button)findViewById(R.id.button_trip_confirm);
        button_confirm.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                startActivity(new Intent(RouteConfirmPopup.this, RouteSuccessActivity.class));
            }
        });


    }




}
