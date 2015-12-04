package se.uu.csproject.monadclient.activities;

import android.content.Context;
import android.os.AsyncTask;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.os.Bundle;
import android.support.v4.content.ContextCompat;
import android.support.v4.view.ViewPager;
import android.support.v7.widget.DefaultItemAnimator;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.SwitchCompat;
import android.support.v7.widget.Toolbar;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CompoundButton;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;

import se.uu.csproject.monadclient.ClientAuthentication;
import se.uu.csproject.monadclient.R;
import se.uu.csproject.monadclient.recyclerviews.LanguageRecyclerViewAdapter;
import se.uu.csproject.monadclient.tabs.SlidingTabLayout;
import se.uu.csproject.monadclient.recyclerviews.Language;

public class SettingsActivity extends MenuedActivity {

    SettingsPagerAdapter settingsPagerAdapter;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        Toolbar toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setHomeAsUpIndicator(R.drawable.ic_home_white_24dp);

        SlidingTabLayout tabs = (SlidingTabLayout) findViewById(R.id.tabs);
        ViewPager pager = (ViewPager) findViewById(R.id.pager);
        settingsPagerAdapter = new SettingsPagerAdapter(getSupportFragmentManager(), SettingsActivity.this);
        pager.setAdapter(settingsPagerAdapter);
        tabs.setDistributeEvenly(true);
        tabs.setSelectedIndicatorColors(ContextCompat.getColor(this.getApplicationContext(), R.color.white));
        tabs.setViewPager(pager);
    }


    @Override
    protected void onStop() {
        super.onStop();

        if(ClientAuthentication.getIfSettingsChanged()){
            UpdateSettingsTask task = new UpdateSettingsTask();

            String response = null;
            try {
                response = task.execute(
                        ClientAuthentication.getClientId(),
                        ClientAuthentication.getLanguage(),
                        ClientAuthentication.getStoreLocation(),
                        ClientAuthentication.getNotificationsAlert(),
                        ClientAuthentication.getRecommendationsAlert(),
                        ClientAuthentication.getTheme()).get();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }

            if(response.startsWith("Success (1)")){
                //Toast.makeText(this, getString(R.string.java_settings_updatesuccess), Toast.LENGTH_LONG).show();
                ClientAuthentication.setIfSettingsChanged(false);
            }
            else{
                //might need to reset alert and recommendation to original user settings since update in the database fails

                //also, this situation: SettingsActivity1 -> ... -> SettingsActivity2, and some settings are changed in SettingsActivity2,
                //then the setting update should be shown in SettingsActivity1 once resumed.
                //however, this is not done yet (and low priority) since it's a bit tricky dealing with fragment
                //Toast.makeText(this, response, Toast.LENGTH_LONG).show();
            }
        }
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if(id == R.id.action_settings){
            return true;
        }
        else {
            return super.onOptionsItemSelected(item);
        }
    }

    public class SettingsPagerAdapter extends FragmentPagerAdapter{
        final int TAB_COUNT = 3; // Language, Alerts, Theme
        private String[] tabTitles;
        Context context;

        public SettingsPagerAdapter(FragmentManager fm, Context context) {
            super(fm);
            tabTitles = getResources().getStringArray(R.array.settings_tab_titles);
            this.context = context;
        }

        @Override
        public Fragment getItem(int position) {
            return SettingsFragment.getInstance(this.context, position + 1);
        }

        @Override
        public CharSequence getPageTitle(int position) {
            return tabTitles[position];
        }

        @Override
        public int getCount() {
            return TAB_COUNT; // GI - number of tabs in the settings view
        }
    }

    public static class SettingsFragment extends Fragment{
        public static final String TAB_POSITION = "tab_position";
        private int page;
        private static Context context;

        public static SettingsFragment getInstance(Context c, int position){
            context = c;
            SettingsFragment settingsFragment = new SettingsFragment();
            Bundle args = new Bundle();
            args.putInt(TAB_POSITION, position);
            settingsFragment.setArguments(args);
            return settingsFragment;
        }

        @Override
        public void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            page = getArguments().getInt(TAB_POSITION);
        }

        @Override
        public void onResume() {
            super.onResume();
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState){
            View layout;

            if(page == 1){
                layout = inflater.inflate(R.layout.fragment_settings_language,container,false);
                List<Language> languages = new ArrayList<>();
                RecyclerView recyclerView = (RecyclerView) layout.findViewById(R.id.recycler_view);
                LinearLayoutManager linearLayoutManager = new LinearLayoutManager(getContext());
                recyclerView.setLayoutManager(linearLayoutManager);
                initializeLanguages(languages);
                LanguageRecyclerViewAdapter adapter = new LanguageRecyclerViewAdapter(context, languages);
                recyclerView.setAdapter(adapter);
                recyclerView.setItemAnimator(new DefaultItemAnimator());
            }
            else if(page == 2){
                layout = inflater.inflate(R.layout.fragment_settings_alerts,container,false);
                final SwitchCompat switchrecommendation;
                final SwitchCompat switchalert;

                // switch button for alerts and recommendations
                switchrecommendation = (SwitchCompat)layout.findViewById(R.id.switch_fragmentsettingsalert_recommendations);
                switchalert = (SwitchCompat)layout.findViewById(R.id.switch_fragmentsettingsalert_alerts);
                if(ClientAuthentication.getRecommendationsAlert().equals("1")) {
                    switchrecommendation.setChecked(true);
                }
                else{
                    switchrecommendation.setChecked(false);
                }

                if(ClientAuthentication.getNotificationsAlert().equals("1")) {
                    switchalert.setChecked(true);
                }
                else{
                    switchalert.setChecked(false);
                }

                switchrecommendation.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                    @Override
                    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                        if(switchrecommendation.isChecked()) {
                            ClientAuthentication.setRecommendationsAlert("1");
                        }
                        else {
                            ClientAuthentication.setRecommendationsAlert("0");
                        }
                        ClientAuthentication.setIfSettingsChanged(true);
                    }
                });

                switchalert.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                    @Override
                    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                        if(switchalert.isChecked()) {
                            ClientAuthentication.setNotificationsAlert("1");
                        }
                        else{
                            ClientAuthentication.setNotificationsAlert("0");
                        }
                        ClientAuthentication.setIfSettingsChanged(true);
                    }
                });
            }
            else if(page == 3){
                layout = inflater.inflate(R.layout.fragment_settings_theme,container,false);
                final RadioGroup radiogroup_themes;
                final RadioButton radiobutton_defaulttheme;
                final RadioButton radiobutton_lighttheme;
                final RadioButton radiobutton_darktheme;

                //different themes
                radiogroup_themes  = (RadioGroup)layout.findViewById(R.id.radiogroup_fragmentsettingstheme_theme);
                radiobutton_defaulttheme = (RadioButton)layout.findViewById(R.id.radiobutton_fragmentsettingstheme_default);
                radiobutton_lighttheme = (RadioButton)layout.findViewById(R.id.radiobutton_fragmentsettingstheme_light);
                radiobutton_darktheme = (RadioButton)layout.findViewById(R.id.radiobutton_fragmentsettingstheme_dark);

                switch (ClientAuthentication.getTheme()){
                    case "0":
                        radiobutton_lighttheme.setChecked(true);
                        break;
                    case "1":
                        radiobutton_defaulttheme.setChecked(true);
                        break;
                    case "2":
                        radiobutton_darktheme.setChecked(true);
                        break;
                }

                radiogroup_themes.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {

                    @Override
                    public void onCheckedChanged(RadioGroup group, int checkedId) {
                        switch (checkedId) {
                            case R.id.radiobutton_fragmentsettingstheme_light:
                                Toast.makeText(getActivity().getApplicationContext(), getString(R.string.java_settings_themechanged_light), Toast.LENGTH_LONG).show();
                                ClientAuthentication.setTheme("0");
                                //change the theme to light
                                break;
                            case R.id.radiobutton_fragmentsettingstheme_default:
                                Toast.makeText(getActivity().getApplicationContext(), getString(R.string.java_settings_themechanged_default), Toast.LENGTH_LONG).show();
                                ClientAuthentication.setTheme("1");
                                //change the theme to default
                                break;
                            case R.id.radiobutton_fragmentsettingstheme_dark:
                                Toast.makeText(getActivity().getApplicationContext(), getString(R.string.java_settings_themechanged_dark), Toast.LENGTH_LONG).show();
                                ClientAuthentication.setTheme("2");
                                //change the theme to dark
                                break;
                        }
                        ClientAuthentication.setIfSettingsChanged(true);
                    }
                });
            }
            else{
                layout = inflater.inflate(R.layout.fragment_settings_theme,container,false);
                //TextView textView = (TextView) layout.findViewById(R.id.themetxt);
                //textView.setText("DEFAULT FRAGMENT FROM THEME");
            }
            return layout;
        }

        private void initializeLanguages(List<Language> languages){
            languages.add(new Language("English", "en", R.drawable.lang_en));
            languages.add(new Language("Svenska", "sv", R.drawable.lang_sv));
            languages.add(new Language("Français", "fr", R.drawable.lang_fr));
            languages.add(new Language("Ελληνικά", "gr", R.drawable.lang_gr));
            languages.add(new Language("Norsk", "no", R.drawable.lang_no));
            languages.add(new Language("中文", "zh", R.drawable.lang_zh));
//            languages.add(new Language("Dansk", "dk", R.drawable.lang_dk));
//            languages.add(new Language("Deutsch", "de", R.drawable.lang_de));
//            languages.add(new Language("Suomi", "fi", R.drawable.lang_fi));
        }
    }

    private static class UpdateSettingsTask extends AsyncTask<String, Void, String>{

        @Override
        protected String doInBackground(String... params) {
            return ClientAuthentication.postSettingsUpdateRequest(params[0], params[1], params[2], params[3], params[4], params[5]);
        }
    }

}

