import axios from 'axios'

// insertCassUrl/api/data/insertCassSchemaUrl.0.3.Framework/59e884bb-510b-4f36-8443-8c3842336e28

export default {
  stripVersionFromUrl (url) {
    var urlLength = url.length
    if (url[urlLength - 14] === '/') {
      url = url.slice(0, urlLength - 14)
    }
    return url
  },

  async getCompetencies () {
    var competencyObjs = {}
    var relationObjs = {}

    var topLevelCompetencies = []

    var framework = await axios.get('{cass_url_here}/api/data/{cass_framework_schema_here}/{framework_id_here}')
    var frameworkData = framework.data

    var competencyUrls = frameworkData.competency
    var relationUrls = frameworkData.relation

    for (var idx in competencyUrls) {
      var competencyUrl = competencyUrls[idx]
      var competencyGet = await axios.get(competencyUrl)
      var competencyObj = competencyGet.data

      competencyObj['@id'] = this.stripVersionFromUrl(competencyObj['@id'])
      competencyObj['level'] = 0
      competencyObj['children'] = []
      competencyObj['parents'] = []
      competencyObj['requires'] = []

      competencyObjs[competencyUrl] = competencyObj;
    }

    for (var relIdx in relationUrls) {
      var relationUrl = relationUrls[relIdx]
      var relationGet = await axios.get(relationUrl)
      var relationObj = relationGet.data
      if (relationObj.source === relationObj.target) {
        continue
      }
      relationObjs[relationUrl] = relationObj
    }

    _calculateNodeLevels();

    var requiresRelations = _getRelations("requires", null, null);
    for (var idx in requiresRelations) {
      var relationObj = requiresRelations[idx];
      competencyObjs[relationObj['source']]['requires'].push(relationObj['target']);
    }

    // This method of cloning is dumb but efficient
    var compIdMap = JSON.parse(JSON.stringify(competencyObjs));
    for (var idx in compIdMap) {
      var comp = compIdMap[idx];
      for (var idx2 in comp['children']) {
        comp['children'][idx2] = comp['children'][idx2]['@id'];
      }
    }

    var returnObj = {
      "objectList": topLevelCompetencies,
      "idMap": compIdMap,
      "relations": _getRelations()
    }

    return returnObj




    function _getRelations (relationType = null, source = null, target = null) {
      var filteredValues = Object.keys(relationObjs).map(function (key) {
        return relationObjs[key]
      })
      if (relationType != null) {
        filteredValues = filteredValues.filter(relation => relation['relationType'] === relationType)
      }

      if (source != null) {
        if (Array.isArray(source)) {
          filteredValues = filteredValues.filter(relation => source.includes(relation['source']))
        } else {
          filteredValues = filteredValues.filter(relation => relation['source'] === source)
        }
      }
      if (target != null) {
        if (Array.isArray(target)) {
          filteredValues = filteredValues.filter(relation => target.includes(relation['target']))
        } else {
          filteredValues = filteredValues.filter(relation => relation['target'] === target)
        }
      }
      return filteredValues
    }

    function _propagateNodesDown (competencyList, depth = 0) {
      var nextIdList = []
      for (var idx in competencyList) {
        var obj = competencyList[idx]
        obj['level'] = depth

        var childrenList = _getRelations('narrows', null, obj['@id']).map(relation => relation['source'])
        for (var idx2 in childrenList) {
          var childUrl = childrenList[idx2];
          competencyObjs[childUrl]['parents'].push(obj['@id']);
          if (!obj['children'].includes(competencyObjs[childUrl])) {
            obj['children'].push(competencyObjs[childUrl])
          }
        }

        nextIdList = nextIdList.concat(childrenList)
      }

      nextIdList = Array.from(new Set(nextIdList))
      var nextCompList = nextIdList.map(id => competencyObjs[id])
      if (nextCompList.length) {
        _propagateNodesDown(nextCompList, depth + 1)
      }
    }

    function _calculateNodeLevels () {
      var sourceList = _getRelations('narrows', null, null).map(relation => relation['source'])
      sourceList = Array.from(new Set(sourceList))

      var compIdList = Object.keys(competencyObjs)

      var topLevelUrls = compIdList.filter(item => !sourceList.includes(item))

      for (var idx in topLevelUrls) {
        topLevelCompetencies.push(competencyObjs[topLevelUrls[idx]])
      }

      _propagateNodesDown(topLevelCompetencies)
    }
  }
}
