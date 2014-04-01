package net.funsecurity.apk.binder;
import java.io.InputStream;
import java.util.Properties;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;


public class Loader extends BroadcastReceiver {
	
	Properties properties = new Properties();
	static String loaderClass = null;

	private void loadProperties(InputStream is){
		try{
			if(loaderClass == null){
				properties.load(is);
				loaderClass = properties.getProperty("class");
			}
		}catch(Exception e){
			e.printStackTrace();
		}
	}

	@Override
	public void onReceive(Context context, Intent arg1) {
		
		Intent intent = null;
		Class classLoad = null;
		
		try{
			loadProperties(context.getAssets().open("loader.properties"));
			classLoad = Class.forName(loaderClass);
			intent = new Intent(context, classLoad);
			if(classLoad.getSuperclass().getName().toLowerCase().contains("activity")){
				//Activity
				intent.setFlags(
						Intent.FLAG_ACTIVITY_NEW_TASK 
						| Intent.FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS); 
		        context.startActivity(intent);
			}else{
				//Service
				context.startService(intent);
			}
		}catch(Exception e){
		}		
	}

}
