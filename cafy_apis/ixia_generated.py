
class Cafy:

    def get_traffic_items_dict(self):
        """
        Get a dictionary of traffic items with keys as Traffic Item Name and values as Traffic Item Type.

        :return: Dictionary of traffic items with keys as Traffic Item Name and values as Traffic Item Type.
                If failed, raise IxiaOperationException.

        :Example: get_traffic_items_dict()
        """
        self.log.info("Retrieving traffic items dictionary")
        traffic_items_dict = {}
        try:
            traffic_items = self.ixNetwork.Traffic.TrafficItem.find()
            for traffic_item in traffic_items:
                traffic_items_dict[traffic_item.Name] = traffic_item.TrafficItemType
            return traffic_items_dict
        except Exception as ex:
            raise IxiaOperationException(f"Failed to retrieve traffic items dictionary: {ex}")

    def create_bgp_router_config(self, topology_name, device_group_name, router_name, as_num, dut_as_num, dut_ipv4_addr):
        """
        Create a BGP router configuration under a device group.

        Args:
            topology_name (str): Name of the topology.
            device_group_name (str): Name of the device group.
            router_name (str): Name of the BGP router.
            as_num (str): AS number for the BGP router.
            dut_as_num (str): DUT AS number.
            dut_ipv4_addr (str): DUT IPv4 address.

        Returns:
            str: Handle to the created BGP router configuration.
        """
        # Get the topology
        topology = self.ixNetwork.Topology.find(Name=topology_name)
        if not topology:
            raise Exception(f"Topology '{topology_name}' not found.")

        # Get the device group
        device_group = topology.DeviceGroup.find(Name=device_group_name)
        if not device_group:
            raise Exception(f"Device group '{device_group_name}' not found in topology '{topology_name}'.")

        # Create BGP router configuration
        bgp_router = device_group.BgpRouterConfig.add()
        bgp_router.Name = router_name
        bgp_router.AsNum = as_num
        bgp_router.DutasNum = dut_as_num
        bgp_router.DutIpv4Addr = dut_ipv4_addr

        return bgp_router

    def add_bgp_ipv4_route(self, bgp_router, route_name, network, prefix_length, as_path=None, community=None, local_pref=None):
        """
        Add a BGP IPv4 route to a BGP router configuration.

        Args:
            bgp_router (str): Handle to the BGP router configuration.
            route_name (str): Name of the BGP route.
            network (str): Network address for the route.
            prefix_length (str): Prefix length for the route.
            as_path (list, optional): AS path for the route.
            community (str, optional): Community attribute for the route.
            local_pref (str, optional): Local preference for the route.

        Returns:
            str: Handle to the created BGP IPv4 route.
        """
        # Create BGP IPv4 route
        bgp_route = bgp_router.BgpIpv4RouteConfig.add()
        bgp_route.Name = route_name

        # Configure network block
        network_block = bgp_route.Ipv4NetworkBlock.add()
        network_block.StartIpList = network
        network_block.PrefixLength = prefix_length
        network_block.NetworkCount = 1

        # Configure AS path if provided
        if as_path:
            bgp_route.AsPath = as_path

        # Configure community if provided
        if community:
            bgp_route.Community = community

        # Configure local preference if provided
        if local_pref:
            bgp_route.LocalPreference = local_pref

        return bgp_route

    def add_bgp_ipv6_route(self, bgp_router, route_name, network, prefix_length, as_path=None, community=None, local_pref=None):
        """
        Add a BGP IPv6 route to a BGP router configuration.

        Args:
            bgp_router (str): Handle to the BGP router configuration.
            route_name (str): Name of the BGP route.
            network (str): Network address for the route.
            prefix_length (str): Prefix length for the route.
            as_path (list, optional): AS path for the route.
            community (str, optional): Community attribute for the route.
            local_pref (str, optional): Local preference for the route.

        Returns:
            str: Handle to the created BGP IPv6 route.
        """
        # Create BGP IPv6 route
        bgp_route = bgp_router.BgpIpv6RouteConfig.add()
        bgp_route.Name = route_name

        # Configure network block
        network_block = bgp_route.Ipv6NetworkBlock.add()
        network_block.StartIpList = network
        network_block.PrefixLength = prefix_length
        network_block.NetworkCount = 1

        # Configure AS path if provided
        if as_path:
            bgp_route.AsPath = as_path

        # Configure community if provided
        if community:
            bgp_route.Community = community

        # Configure local preference if provided
        if local_pref:
            bgp_route.LocalPreference = local_pref

        return bgp_route

    def create_traffic_stream(self, topology_name, device_group_name, stream_name, source_device, destination_routes):
        """
        Create a traffic stream between source and destination routes.

        Args:
            topology_name (str): Name of the topology.
            device_group_name (str): Name of the device group.
            stream_name (str): Name of the traffic stream.
            source_device (str): Handle to the source device.
            destination_routes (list): List of destination route handles.

        Returns:
            str: Handle to the created traffic stream.
        """
        # Get the topology
        topology = self.ixNetwork.Topology.find(Name=topology_name)
        if not topology:
            raise Exception(f"Topology '{topology_name}' not found.")

        # Get the device group
        device_group = topology.DeviceGroup.find(Name=device_group_name)
        if not device_group:
            raise Exception(f"Device group '{device_group_name}' not found in topology '{topology_name}'.")

        # Create traffic stream
        traffic_stream = self.ixNetwork.Traffic.TrafficItem.add()
        traffic_stream.Name = stream_name

        # Configure source and destination bindings
        source_binding = source_device
        destination_binding = " ".join(destination_routes)

        traffic_stream.EndpointSet.add(SrcBinding=source_binding, DstBinding=destination_binding)

        return traffic_stream

    def get_device_group_names_from_port(self, port_name=None):
        """
        Retrieve device group names associated with a specific port or all ports.

        Args:
            port_name (str, optional): The name of the port to query. If None, returns device groups for all ports.

        Returns:
            dict: A dictionary where keys are port names and values are lists of device group names.
                If `port_name` is provided, the dictionary will contain only that port.
        """
        device_group_info = {}

        if port_name:
            vport = self.ixNetwork.Vport.find(Name=port_name)
            if not vport:
                return device_group_info

            vport_href = vport.href
            device_group_names = []

            for topology in self.ixNetwork.Topology.find():
                if vport_href in topology.Vports:
                    device_group_names.extend([dg.Name for dg in topology.DeviceGroup.find()])

            device_group_info[port_name] = device_group_names
        else:
            for vport in self.ixNetwork.Vport.find():
                vport_href = vport.href
                device_group_names = []

                for topology in self.ixNetwork.Topology.find():
                    if vport_href in topology.Vports:
                        device_group_names.extend([dg.Name for dg in topology.DeviceGroup.find()])

                device_group_info[vport.Name] = device_group_names

        return device_group_info

    def get_device_names(self, port_name=None):
        """
        Get device names associated with a port or all ports, including nested device groups.

        :param port_name: Name of the port or list of port names. If None, all ports are considered.
        :return: Dictionary with port names as keys and lists of device group names as values.
        """
        device_group_info = {}

        def get_nested_device_groups(topology, vport_href):
            """
            Recursively retrieve device group names, including nested ones.

            :param topology: Topology object.
            :param vport_href: Href of the vport.
            :return: List of device group names.
            """
            device_group_names = []

            for device_group in topology.DeviceGroup.find():
                if vport_href in device_group.Vports:
                    device_group_names.append(device_group.Name)

                # Check for nested device groups
                for network_group in device_group.NetworkGroup.find():
                    for nested_device_group in network_group.DeviceGroup.find():
                        if vport_href in nested_device_group.Vports:
                            device_group_names.append(nested_device_group.Name)

            return device_group_names

        if port_name:
            if isinstance(port_name, str):
                port_name = [port_name]

            for port in port_name:
                vport = self.ixNetwork.Vport.find(Name=f"^{re.escape(port)}$")
                if not vport:
                    continue

                vport_href = vport.href
                device_group_names = []

                for topology in self.ixNetwork.Topology.find():
                    if vport_href in topology.Vports:
                        device_group_names.extend(get_nested_device_groups(topology, vport_href))

                device_group_info[port] = device_group_names

        else:
            for vport in self.ixNetwork.Vport.find():
                vport_href = vport.href
                device_group_names = []

                for topology in self.ixNetwork.Topology.find():
                    if vport_href in topology.Vports:
                        device_group_names.extend(get_nested_device_groups(topology, vport_href))

                device_group_info[vport.Name] = device_group_names

        return device_group_info



    def find_rocev2_name(self, topology_name=None, device_group_name=None):
        """
        Find and return the names of all RoCEv2 and RoCEv6 stacks across all device groups,
        including two-level device groups. This API traverses the entire configuration and
        collects the names of RoCEv2 and RoCEv6 stacks under IPv4, IPv6, IPv4Loopback, or IPv6Loopback.

        Args:
            topology_name (str, optional): Name of the topology. If None, applies to all topologies.
            device_group_name (str, optional): Name of the device group. If None, applies to all device groups.

        Returns:
            list: List of RoCEv2 and RoCEv6 stack names.

        Example:
            find_rocev2_name(topology_name="Topology1", device_group_name="DeviceGroup1")
            find_rocev2_name()
        """
        self.log.info("Finding RoCEv2 and RoCEv6 stack names across all device groups")
        roce_stack_names = []

        try:
            if topology_name:
                topologies = [self.ixNetwork.Topology.find(Name=topology_name)]
                if not topologies:
                    raise IxiaOperationException(f"Topology '{topology_name}' not found.")
            else:
                topologies = self.ixNetwork.Topology.find()
                if not topologies:
                    raise IxiaOperationException("No topologies found in the configuration.")

            for topology in topologies:
                if device_group_name:
                    device_groups = [topology.DeviceGroup.find(Name=device_group_name)]
                    if not device_groups:
                        raise IxiaOperationException(f"Device group '{device_group_name}' not found in topology '{topology.Name}'.")
                else:
                    device_groups = topology.DeviceGroup.find()
                    if not device_groups:
                        self.log.warning(f"No device groups found in topology '{topology.Name}'.")
                        continue

                for device_group in device_groups:
                    # Check for nested device groups (two-level)
                    nested_device_groups = device_group.DeviceGroup.find()
                    if nested_device_groups:
                        for nested_dg in nested_device_groups:
                            self._collect_roce_stack_names(nested_dg, roce_stack_names)
                    else:
                        self._collect_roce_stack_names(device_group, roce_stack_names)

                    # Check for network groups (two-level)
                    network_groups = device_group.NetworkGroup.find()
                    for network_group in network_groups:
                        inner_device_groups = network_group.DeviceGroup.find()
                        for inner_device_group in inner_device_groups:
                            self._collect_roce_stack_names(inner_device_group, roce_stack_names)

            if not roce_stack_names:
                self.log.warning("No RoCEv2 or RoCEv6 stacks found in the configuration.")

            return roce_stack_names
        except Exception as ex:
            raise IxiaOperationException(f"Failed to find RoCEv2 and RoCEv6 stack names: {ex}")

    def _collect_roce_stack_names(self, device_group, roce_stack_names):
        """
        Internal method to collect RoCEv2 and RoCEv6 stack names from a device group.
        Checks under IPv4, IPv6, IPv4Loopback, or IPv6Loopback for RoCE stacks.

        Args:
            device_group: Device group object.
            roce_stack_names (list): List to store RoCE stack names.
        """
        # Check IPv4 for RoCEv2
        try:
            ipv4_list = device_group.Ethernet.find().Ipv4.find()
            for ipv4 in ipv4_list:
                rocev2_list = ipv4.Rocev2.find()
                for rocev2 in rocev2_list:
                    roce_stack_names.append(rocev2.Name)
        except Exception:
            pass  # IPv4 or RoCEv2 not found, move on

        # Check IPv6 for RoCEv6
        try:
            ipv6_list = device_group.Ethernet.find().Ipv6.find()
            for ipv6 in ipv6_list:
                rocev6_list = ipv6.Rocev6.find()
                for rocev6 in rocev6_list:
                    roce_stack_names.append(rocev6.Name)
        except Exception:
            pass  # IPv6 or RoCEv6 not found, move on

        # Check IPv4Loopback for RoCEv2
        try:
            ipv4_loopback_list = device_group.Ethernet.find().Ipv4Loopback.find()
            for ipv4_loopback in ipv4_loopback_list:
                rocev2_list = ipv4_loopback.Rocev2.find()
                for rocev2 in rocev2_list:
                    roce_stack_names.append(rocev2.Name)
        except Exception:
            pass

    def get_rocev2_names(self):
        """
        Retrieves the names of all RoCEv2 and RoCEv6 stacks across all device groups,
        including two-level device groups. This method checks for RoCE stacks under
        IPv4, IPv6, IPv4Loopback, and IPv6Loopback.

        Returns:
            list: A list of RoCEv2 and RoCEv6 stack names.
        """
        roce_names = []

        # Iterate through all topologies
        for topology in self.ixNetwork.Topology.find():
            # Iterate through all device groups in the topology
            for device_group in topology.DeviceGroup.find():
                # Check for RoCEv2 under IPv4
                try:
                    ipv4_list = device_group.Ethernet.find().Ipv4.find()
                    for ipv4 in ipv4_list:
                        rocev2 = ipv4.Rocev2.find()
                        if rocev2:
                            for stack in rocev2:
                                roce_names.append(stack.Name)
                except Exception:
                    pass  # IPv4 or RoCEv2 not found, move on

                # Check for RoCEv6 under IPv6
                try:
                    ipv6_list = device_group.Ethernet.find().Ipv6.find()
                    for ipv6 in ipv6_list:
                        rocev6 = ipv6.Rocev6.find()
                        if rocev6:
                            for stack in rocev6:
                                roce_names.append(stack.Name)
                except Exception:
                    pass  # IPv6 or RoCEv6 not found, move on

                # Check for RoCEv2 under IPv4Loopback
                try:
                    ipv4_loopback_list = device_group.Ipv4Loopback.find()
                    for ipv4_loopback in ipv4_loopback_list:
                        rocev2 = ipv4_loopback.Rocev2.find()
                        if rocev2:
                            for stack in rocev2:
                                roce_names.append(stack.Name)
                except Exception:
                    pass  # IPv4Loopback or RoCEv2 not found, move on

                # Check for RoCEv6 under IPv6Loopback
                try:
                    ipv6_loopback_list = device_group.Ipv6Loopback.find()
                    for ipv6_loopback in ipv6_loopback_list:
                        rocev6 = ipv6_loopback.Rocev6.find()
                        if rocev6:
                            for stack in rocev6:
                                roce_names.append(stack.Name)
                except Exception:
                    pass  # IPv6Loopback or RoCEv6 not found, move on

                # Check for nested device groups (two-level)
                for nested_device_group in device_group.DeviceGroup.find():
                    # Check for RoCEv2 under IPv4 in nested device group
                    try:
                        ipv4_list = nested_device_group.Ethernet.find().Ipv4.find()
                        for ipv4 in ipv4_list:
                            rocev2 = ipv4.Rocev2.find()
                            if rocev2:
                                for stack in rocev2:
                                    roce_names.append(stack.Name)
                    except Exception:
                        pass  # IPv4 or RoCEv2 not found, move on

                    # Check for RoCEv6 under IPv6 in nested device group
                    try:
                        ipv6_list = nested_device_group.Ethernet.find().Ipv6.find()
                        for ipv6 in ipv6_list:
                            rocev6 = ipv6.Rocev6.find()
                            if rocev6:
                                for stack in rocev6:
                                    roce_names.append(stack.Name)
                    except Exception:
                        pass  # IPv6 or RoCEv6 not found, move on

                    # Check for RoCEv2 under IPv4Loopback in nested device group
                    try:
                        ipv4_loopback_list = nested_device_group.Ipv4Loopback.find()
                        for ipv4_loopback in ipv4_loopback_list:
                            rocev2 = ipv4_loopback.Rocev2.find()
                            if rocev2:
                                for stack in rocev2:
                                    roce_names.append(stack.Name)
                    except Exception:
                        pass  # IPv4Loopback or RoCEv2 not found, move on

                    # Check for RoCEv6 under IPv6Loopback in nested device group
                    try:
                        ipv6_loopback_list = nested_device_group.Ipv6Loopback.find()
                        for ipv6_loopback in ipv6_loopback_list:
                            rocev6 = ipv6_loopback.Rocev6.find()
                            if rocev6:
                                for stack in rocev6:
                                    roce_names.append(stack.Name)
                    except Exception:
                        pass  # IPv6Loopback or RoCEv6 not found, move
