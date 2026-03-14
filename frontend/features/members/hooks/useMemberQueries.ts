/**
 * Member hooks using React Query
 */
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { memberService } from "../services/member.service";
import { CreateMemberData, UpdateMemberData, CreateLeadData } from "../types";
import { toast } from "sonner";

// Query keys
export const memberKeys = {
  all: ["members"] as const,
  lists: () => [...memberKeys.all, "list"] as const,
  list: (params?: any) => [...memberKeys.lists(), params] as const,
  details: () => [...memberKeys.all, "detail"] as const,
  detail: (id: string) => [...memberKeys.details(), id] as const,
  stats: () => [...memberKeys.all, "stats"] as const,
  search: (query: string) => [...memberKeys.all, "search", query] as const,
};

export const leadKeys = {
  all: ["leads"] as const,
  lists: () => [...leadKeys.all, "list"] as const,
  list: (params?: any) => [...leadKeys.lists(), params] as const,
  details: () => [...leadKeys.all, "detail"] as const,
  detail: (id: string) => [...leadKeys.details(), id] as const,
  stats: () => [...leadKeys.all, "stats"] as const,
};

/**
 * Hook to get members list
 */
export function useMembers(params?: {
  page?: number;
  pageSize?: number;
  status?: string;
  search?: string;
}) {
  return useQuery({
    queryKey: memberKeys.list(params),
    queryFn: () => memberService.getMembers(params),
  });
}

/**
 * Hook to get single member
 */
export function useMember(id: string) {
  return useQuery({
    queryKey: memberKeys.detail(id),
    queryFn: () => memberService.getMember(id),
    enabled: !!id,
  });
}

/**
 * Hook to get member stats
 */
export function useMemberStats() {
  return useQuery({
    queryKey: memberKeys.stats(),
    queryFn: () => memberService.getMemberStats(),
  });
}

/**
 * Hook to search members
 */
export function useSearchMembers(query: string) {
  return useQuery({
    queryKey: memberKeys.search(query),
    queryFn: () => memberService.searchMembers(query),
    enabled: query.length >= 2,
  });
}

/**
 * Hook to create member
 */
export function useCreateMember() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateMemberData) => memberService.createMember(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: memberKeys.lists() });
      queryClient.invalidateQueries({ queryKey: memberKeys.stats() });
      toast.success("Member created successfully");
    },
    onError: (error: any) => {
      toast.error(error.message || "Failed to create member");
    },
  });
}

/**
 * Hook to update member
 */
export function useUpdateMember() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateMemberData }) =>
      memberService.updateMember(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: memberKeys.detail(variables.id) });
      queryClient.invalidateQueries({ queryKey: memberKeys.lists() });
      queryClient.invalidateQueries({ queryKey: memberKeys.stats() });
      toast.success("Member updated successfully");
    },
    onError: (error: any) => {
      toast.error(error.message || "Failed to update member");
    },
  });
}

/**
 * Hook to delete member
 */
export function useDeleteMember() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => memberService.deleteMember(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: memberKeys.lists() });
      queryClient.invalidateQueries({ queryKey: memberKeys.stats() });
      toast.success("Member deleted successfully");
    },
    onError: (error: any) => {
      toast.error(error.message || "Failed to delete member");
    },
  });
}

/**
 * Hook to activate member
 */
export function useActivateMember() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => memberService.activateMember(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: memberKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: memberKeys.lists() });
      queryClient.invalidateQueries({ queryKey: memberKeys.stats() });
      toast.success("Member activated successfully");
    },
  });
}

/**
 * Hook to deactivate member
 */
export function useDeactivateMember() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => memberService.deactivateMember(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: memberKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: memberKeys.lists() });
      queryClient.invalidateQueries({ queryKey: memberKeys.stats() });
      toast.success("Member deactivated successfully");
    },
  });
}

/**
 * Hook to suspend member
 */
export function useSuspendMember() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => memberService.suspendMember(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: memberKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: memberKeys.lists() });
      queryClient.invalidateQueries({ queryKey: memberKeys.stats() });
      toast.success("Member suspended successfully");
    },
  });
}

// Lead Hooks

/**
 * Hook to get leads list
 */
export function useLeads(params?: {
  page?: number;
  pageSize?: number;
  status?: string;
  search?: string;
}) {
  return useQuery({
    queryKey: leadKeys.list(params),
    queryFn: () => memberService.getLeads(params),
  });
}

/**
 * Hook to get single lead
 */
export function useLead(id: string) {
  return useQuery({
    queryKey: leadKeys.detail(id),
    queryFn: () => memberService.getLead(id),
    enabled: !!id,
  });
}

/**
 * Hook to get lead stats
 */
export function useLeadStats() {
  return useQuery({
    queryKey: leadKeys.stats(),
    queryFn: () => memberService.getLeadStats(),
  });
}

/**
 * Hook to create lead
 */
export function useCreateLead() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateLeadData) => memberService.createLead(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: leadKeys.lists() });
      queryClient.invalidateQueries({ queryKey: leadKeys.stats() });
      toast.success("Lead created successfully");
    },
    onError: (error: any) => {
      toast.error(error.message || "Failed to create lead");
    },
  });
}

/**
 * Hook to update lead
 */
export function useUpdateLead() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<CreateLeadData> }) =>
      memberService.updateLead(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: leadKeys.detail(variables.id) });
      queryClient.invalidateQueries({ queryKey: leadKeys.lists() });
      toast.success("Lead updated successfully");
    },
    onError: (error: any) => {
      toast.error(error.message || "Failed to update lead");
    },
  });
}

/**
 * Hook to convert lead to member
 */
export function useConvertLead() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: CreateMemberData }) =>
      memberService.convertLead(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: leadKeys.lists() });
      queryClient.invalidateQueries({ queryKey: leadKeys.stats() });
      queryClient.invalidateQueries({ queryKey: memberKeys.lists() });
      queryClient.invalidateQueries({ queryKey: memberKeys.stats() });
      toast.success("Lead converted to member successfully");
    },
    onError: (error: any) => {
      toast.error(error.message || "Failed to convert lead");
    },
  });
}