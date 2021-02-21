$(document).ready(function() {
  var network;
  var node_urls = {};

  var root_url = "http://en.wikipedia.org/wiki/";
  if(window.location.protocol === "https:")
    root_url = "https://en.wikipedia.org/wiki/";

  function loadWikipediaPage(nodeId) {
    var options = {};
    if(nodeId >= 0) {
      var options = {
        edges: {
          color: {
            inherit: false,
            color:  '#454d54',
            highlight: '#33d6ff'
          }
        }
      };
      $('#detail').attr('src', root_url + node_urls[nodeId]);
    }
    else {
      options = {
        edges: {
          color: {
            inherit: "both"
          },
        }
      };
      $('#detail').attr('src', 'about:blank');
    }
    network.setOptions(options);
  }

  function redrawAll(nodes, edges) {
    var container = document.getElementById('graph');
    var data = {
      nodes: nodes,
      edges: edges
    };
    var options = {
      nodes: {
        shape: 'dot',
        scaling: {
          min: 10,
          max: 30
        },
        font: {
          size: 12,
          color: "#ffffff",
          face: 'Tahoma'
        }
      },
      edges: {
        width: 0.1,
        selectionWidth: 10,
        color: {
          inherit: "both"
        },
        smooth: {
          type: 'continuous'
        },
        arrows: {
          to: true
        }
      },
      physics: {
        //stabilization: true,
        stabilization: {
          iterations: 500
        },
        barnesHut: {
          gravitationalConstant: -80000,
          springConstant: 0.001,
          springLength: 200
        }
      },
      interaction: {
        tooltipDelay: 200,
        hideEdgesOnDrag: true
      },
      layout: {
        improvedLayout: false
      }
    };

    network = new vis.Network(container, data, options);

    network.on('click', function(properties) {
      var ids = properties.nodes;
      if(ids.length > 0) {
        $("#artist_select").val(ids[0]);
        loadWikipediaPage(ids[0]);
      }
      else {
        $("#artist_select").val(-1);
        loadWikipediaPage(-1);
      }
    });

    network.on('stabilizationIterationsDone', function(properties) {
      $.ajax({
        url: `${window.location.origin}/positions`,
        method: "POST",
        headers: {"Content-Type": "application/json"},
        data: JSON.stringify(network.getPositions())
      });
    });
  }

  $("#artist_select").change(function (e) {
    var selectedArtist = $('#artist_select').val();
    if(selectedArtist >= 0) {
      network.selectNodes([selectedArtist]);
      loadWikipediaPage(selectedArtist);
    }
    else {$("#detail")
      network.selectNodes([]);
      loadWikipediaPage(selectedArtist);
    }
  });

  function fill_options(nodes){
    var sorted_nodes = _.sortBy(nodes, 'label');
    var options = sorted_nodes.map(n => "<option value='" + n.id + "'>" + n.label + "</option>");
    $("#artist_select").html("<option value='-1'>Select a musician or band</option>" + options.join(""));
  }

  if(!window.hasOwnProperty("nodes") || !window.hasOwnProperty("edges")) {
    $.ajax({
      url: `${window.location.origin}/graph`,
      method: "GET",
      success: function (response) {
        nodes = response.nodes;
        edges = response.edges;

        fill_options(nodes);
        node_urls = _.object(_.map(nodes, (n) => {return [n.id, n.url]}));
        redrawAll(nodes, edges);
      }
    });
  } else {
    fill_options(nodes);
    node_urls = _.object(_.map(nodes, (n) => {return [n.id, n.url]}));
    redrawAll(nodes, edges);
  }
});