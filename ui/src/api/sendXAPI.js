export default {
  async sendLaunched (userInfo, activity) {
    // Set the config
    await this.setConfig('lrs')

    // Build the statement
    stmt = {}
    stmt.verb = ADL.verbs.launched;
    let stmt = await this.buildActivityStatement(stmt, this.getFullName(userInfo), userInfo.id, activity);

    // Send it
    console.log('sending launched xapi', stmt)
    ADL.XAPIWrapper.sendStatement(stmt, function () {});
  },
  async sendGoalSet(userInfo, competencyId) {
    // Set the config
    await this.setConfig('lrs')

    // Build the statement
    stmt = {}
    stmt.verb = ADL.verbs['chose'];
    let stmt = await this.buildStatement(stmt, this.getFullName(userInfo), userInfo.id);

    stmt.object = {
      'objectType': 'Activity',
      'id': '{fluent_server_here}/choose-goal',
      'definition': {
        'name': {
          'en': 'Choose Goal'
        },
        'extensions': {
          '{fluent_server_here}:8979/recommender/goal-data': {
            'competencyId': competencyId
          }
        }
      }
    }

    // Send it
    console.log('sending goal set xapi', stmt)
    ADL.XAPIWrapper.sendStatement(stmt, function () {});
  },
  async sendRecommendationOrdering(userInfo, orderedActivities) {
    if (userInfo === undefined || userInfo.id === undefined || userInfo.id === '' || orderedActivities === undefined || orderedActivities.length === 0) {
      return
    }
    // set the config
    await this.setConfig('logging_lrs')
    
    stmt = {}
    stmt.verb = ADL.verbs['received']
    let stmt = await this.buildStatement(stmt, this.getFullName(userInfo), userInfo.id);

    stmt.object = {
      'objectType': 'Activity',
      'id': '{fluent_server_here}/sorted-activities',
      'definition': {
        'name': {
          'en': 'Sorted Activities'
        },
        'extensions': {
          '{fluent_server_here}:8979/recommender/log-data': {
            'learnerId': userInfo.id,
            'sortedActivities': orderedActivities
          }
        }
      }
    }
    console.log('sending recommendation ordering xapi', stmt)
    ADL.XAPIWrapper.sendStatement(stmt, function () {});
  },
  async sendRecommendations(userInfo, reccs) {
    // Just return if the user isn't set or there are no reccs
    // (Was getting some weird blank statements)
    if (userInfo === undefined || userInfo.id === undefined || userInfo.id === '' ||
      reccs === undefined || reccs.length === 0)
      return

    // Set the config
    await this.setConfig('logging_lrs')

    // Build the statement
    stmt = {}
    stmt.verb = ADL.verbs['recommended'];
    let stmt = await this.buildStatement(stmt, this.getFullName(userInfo), userInfo.id);

    // Set array of recommendationRows
    let recommendationRowArr = reccs.recommendations

    stmt.object = {
      'objectType': 'Activity',
      'id': '{fluent_server_here}/recommend-activities',
      'definition': {
        'name': {
          'en': 'Recommend Activities'
        },
        'extensions': {
          '{fluent_server_here}:8979/recommender/log-data': {
            'learnerId': userInfo.id,
            'recommendations': recommendationRowArr
          }
        }
      }
    }

    // Send it
    console.log('sending recommendations xapi', stmt)
    ADL.XAPIWrapper.sendStatement(stmt, function () {});
  },
  async sendLoggedIn(userInfo) {
    // Set the config
    await this.setConfig('lrs')

    // Build the statement
    stmt = {}
    stmt.verb = ADL.verbs['logged-in'];
    let stmt = await this.buildStatement(stmt, this.getFullName(userInfo), userInfo.id);

    // Set the object
    stmt.object = {
      'objectType': 'Activity',
      'id': '{fluent_server_here}:8004/',
      'definition': {
        'name': {
          'en': 'RecommenderUI'
        }
      }
    }

    // Send it
    console.log('sending loggedin xapi', stmt)
    ADL.XAPIWrapper.sendStatement(stmt, function () {});
  },
  async sendLoggedOut(userInfo) {
    // Set the config
    await this.setConfig('lrs')

    // Build the statement
    stmt = {}
    stmt.verb = ADL.verbs['logged-out'];
    let stmt = await this.buildStatement(stmt, this.getFullName(userInfo), userInfo.id);

    // Set the object
    stmt.object = {
      'objectType': 'Activity',
      'id': '{fluent_server_here}:8004/',
      'definition': {
        'name': {
          'en': 'RecommenderUI'
        }
      }
    }

    // Send it
    console.log('sending loggedout xapi', stmt)
    ADL.XAPIWrapper.sendStatement(stmt, function () {});
  },
  // Build the user's name (First Last) as a single string.
  getFullName(userInfo) {
    return (userInfo.firstName + ' ' + userInfo.lastName).trim()
  },
  buildStatement(stmt, kcName, kcUID) {
    var stmt = stmt
    stmt.actor = {
      'name': kcName,
      'account': {
        'homePage': '{keycloak_server_here}:8081/auth/',
        'name': kcUID
      }
    }
    stmt.context = {
      'contextActivities': {
        'category': [{
          'id': 'https://w3id.org/xapi/adl/v1.0',
          'definition': {
            'type': 'http://adlnet.gov/expapi/activities/profile'
          }
        }]
      }
    }
    stmt.timestamp = (new Date()).toISOString();
    return stmt;
  },
  buildActivityStatement(stmt, kcName, kcUID, activity) {
    var stmt = this.buildStatement(stmt, kcName, kcUID)

    // Add the activity Data
    stmt.object = {
      'objectType': 'Activity',
      'id': activity.identifier
    }
    // This was old stuff from the video-player?
    //stmt.object = {'id': activity.identifier, 'definition':{'name': {'en-US': activity.name}}}
    //stmt.context = {'contextActivities':{'parent':[{'id': 'activity:' + activity.identifier}]}}

    // Return
    return stmt
  },
  setConfig(lrsType) {

    // TODO: Do this better so we aren't re-querying the discovery service for every xapi call

    // Get the endpoints for our activity index and the lrs
    // Add a / to the LRS for the xapi wrapper's syntax
    var lrsEndpoint = this.getEndpoint(lrsType) + '/';
    var actEndpoint = this.getEndpoint('activity_index');

    // LRS Statement Credentials
    var auth = this.getAuth(lrsType);

    var config = {
      'identityProviderName': '{keycloak_server_here}:8081/auth/',
      'endpoint': lrsEndpoint,
      'auth': 'Basic ' + auth,
      'activityIndexEndpoint': actEndpoint
    }

    ADL.XAPIWrapper.changeConfig(config);
  },
  getEndpoint(lrsType) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('GET', '{keycloak_server_here}:8085/list/' + lrsType + '/endpoint', false);
    xmlHttp.setRequestHeader('Content-Type', 'text/plain');
    xmlHttp.send(null);
    return xmlHttp.responseText;
  },
  getAuth(lrsType) {
    if (lrsType === 'lrs')
      return '{lrs_auth_here}'
    else if (lrsType === 'logging_lrs')
      return '{lrs_auth_here}'
    else
      return undefined
  }
}
